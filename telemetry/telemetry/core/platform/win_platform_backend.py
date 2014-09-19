# Copyright 2013 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import atexit
import collections
import contextlib
import ctypes
import os
import platform
import re
import socket
import struct
import subprocess
import sys
import time
import zipfile

from telemetry import decorators
from telemetry.core import exceptions
from telemetry.core import util
from telemetry.core.platform import desktop_platform_backend
from telemetry.core.platform import platform_backend
from telemetry.core.platform.power_monitor import msr_power_monitor
from telemetry.util import cloud_storage
from telemetry.util import path

try:
  import pywintypes  # pylint: disable=F0401
  import win32api  # pylint: disable=F0401
  from win32com.shell import shell  # pylint: disable=F0401
  from win32com.shell import shellcon  # pylint: disable=F0401
  import win32con  # pylint: disable=F0401
  import win32process  # pylint: disable=F0401
  import win32security  # pylint: disable=F0401
except ImportError:
  pywintypes = None
  shell = None
  shellcon = None
  win32api = None
  win32con = None
  win32process = None
  win32security = None


def _InstallWinRing0():
  """WinRing0 is used for reading MSRs."""
  executable_dir = os.path.dirname(sys.executable)

  python_is_64_bit = sys.maxsize > 2 ** 32
  dll_file_name = 'WinRing0x64.dll' if python_is_64_bit else 'WinRing0.dll'
  dll_path = os.path.join(executable_dir, dll_file_name)

  os_is_64_bit = 'PROGRAMFILES(X86)' in os.environ
  driver_file_name = 'WinRing0x64.sys' if os_is_64_bit else 'WinRing0.sys'
  driver_path = os.path.join(executable_dir, driver_file_name)

  # Check for WinRing0 and download if needed.
  if not (os.path.exists(dll_path) and os.path.exists(driver_path)):
    win_binary_dir = os.path.join(path.GetTelemetryDir(), 'bin', 'win')
    zip_path = os.path.join(win_binary_dir, 'winring0.zip')
    cloud_storage.GetIfChanged(zip_path, bucket=cloud_storage.PUBLIC_BUCKET)
    try:
      with zipfile.ZipFile(zip_path, 'r') as zip_file:
        # Install DLL.
        if not os.path.exists(dll_path):
          zip_file.extract(dll_file_name, executable_dir)
        # Install kernel driver.
        if not os.path.exists(driver_path):
          zip_file.extract(driver_file_name, executable_dir)
    finally:
      os.remove(zip_path)


def IsCurrentProcessElevated():
  handle = win32process.GetCurrentProcess()
  with contextlib.closing(
      win32security.OpenProcessToken(handle, win32con.TOKEN_QUERY)) as token:
    return bool(
        win32security.GetTokenInformation(token, win32security.TokenElevation))


def TerminateProcess(process_handle):
  if not process_handle:
    return
  if win32process.GetExitCodeProcess(process_handle) == win32con.STILL_ACTIVE:
    win32process.TerminateProcess(process_handle, 0)
  process_handle.close()


class WinPlatformBackend(desktop_platform_backend.DesktopPlatformBackend):
  def __init__(self):
    super(WinPlatformBackend, self).__init__()
    self._msr_server_handle = None
    self._msr_server_port = None
    self._power_monitor = msr_power_monitor.MsrPowerMonitor(self)

  def __del__(self):
    self.close()

  def close(self):
    self.CloseMsrServer()

  def CloseMsrServer(self):
    if not self._msr_server_handle:
      return

    TerminateProcess(self._msr_server_handle)
    self._msr_server_handle = None
    self._msr_server_port = None

  # pylint: disable=W0613
  def StartRawDisplayFrameRateMeasurement(self):
    raise NotImplementedError()

  def StopRawDisplayFrameRateMeasurement(self):
    raise NotImplementedError()

  def GetRawDisplayFrameRateMeasurements(self):
    raise NotImplementedError()

  def IsThermallyThrottled(self):
    raise NotImplementedError()

  def HasBeenThermallyThrottled(self):
    raise NotImplementedError()

  def GetSystemCommitCharge(self):
    performance_info = self._GetPerformanceInfo()
    return performance_info.CommitTotal * performance_info.PageSize / 1024

  @decorators.Cache
  def GetSystemTotalPhysicalMemory(self):
    performance_info = self._GetPerformanceInfo()
    return performance_info.PhysicalTotal * performance_info.PageSize / 1024

  def GetCpuStats(self, pid):
    cpu_info = self._GetWin32ProcessInfo(win32process.GetProcessTimes, pid)
    # Convert 100 nanosecond units to seconds
    cpu_time = (cpu_info['UserTime'] / 1e7 +
                cpu_info['KernelTime'] / 1e7)
    return {'CpuProcessTime': cpu_time}

  def GetCpuTimestamp(self):
    """Return current timestamp in seconds."""
    return {'TotalTime': time.time()}

  def GetMemoryStats(self, pid):
    memory_info = self._GetWin32ProcessInfo(
        win32process.GetProcessMemoryInfo, pid)
    return {'VM': memory_info['PagefileUsage'],
            'VMPeak': memory_info['PeakPagefileUsage'],
            'WorkingSetSize': memory_info['WorkingSetSize'],
            'WorkingSetSizePeak': memory_info['PeakWorkingSetSize']}

  def GetIOStats(self, pid):
    io_stats = self._GetWin32ProcessInfo(win32process.GetProcessIoCounters, pid)
    return {'ReadOperationCount': io_stats['ReadOperationCount'],
            'WriteOperationCount': io_stats['WriteOperationCount'],
            'ReadTransferCount': io_stats['ReadTransferCount'],
            'WriteTransferCount': io_stats['WriteTransferCount']}

  def KillProcess(self, pid, kill_process_tree=False):
    # os.kill for Windows is Python 2.7.
    cmd = ['taskkill', '/F', '/PID', str(pid)]
    if kill_process_tree:
      cmd.append('/T')
    subprocess.Popen(cmd, stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT).communicate()

  def GetSystemProcessInfo(self):
    # [3:] To skip 2 blank lines and header.
    lines = subprocess.Popen(
        ['wmic', 'process', 'get',
         'CommandLine,CreationDate,Name,ParentProcessId,ProcessId',
         '/format:csv'],
        stdout=subprocess.PIPE).communicate()[0].splitlines()[3:]
    process_info = []
    for line in lines:
      if not line:
        continue
      parts = line.split(',')
      pi = {}
      pi['ProcessId'] = int(parts[-1])
      pi['ParentProcessId'] = int(parts[-2])
      pi['Name'] = parts[-3]
      creation_date = None
      if parts[-4]:
        creation_date = float(re.split('[+-]', parts[-4])[0])
      pi['CreationDate'] = creation_date
      pi['CommandLine'] = ','.join(parts[1:-4])
      process_info.append(pi)
    return process_info

  def GetChildPids(self, pid):
    """Retunds a list of child pids of |pid|."""
    ppid_map = collections.defaultdict(list)
    creation_map = {}
    for pi in self.GetSystemProcessInfo():
      ppid_map[pi['ParentProcessId']].append(pi['ProcessId'])
      if pi['CreationDate']:
        creation_map[pi['ProcessId']] = pi['CreationDate']

    def _InnerGetChildPids(pid):
      if not pid or pid not in ppid_map:
        return []
      ret = [p for p in ppid_map[pid] if creation_map[p] >= creation_map[pid]]
      for child in ret:
        if child == pid:
          continue
        ret.extend(_InnerGetChildPids(child))
      return ret

    return _InnerGetChildPids(pid)

  def GetCommandLine(self, pid):
    for pi in self.GetSystemProcessInfo():
      if pid == pi['ProcessId']:
        return pi['CommandLine']
    raise exceptions.ProcessGoneException()

  def GetOSName(self):
    return 'win'

  @decorators.Cache
  def GetOSVersionName(self):
    os_version = platform.uname()[3]

    if os_version.startswith('5.1.'):
      return platform_backend.XP
    if os_version.startswith('6.0.'):
      return platform_backend.VISTA
    if os_version.startswith('6.1.'):
      return platform_backend.WIN7
    if os_version.startswith('6.2.'):
      return platform_backend.WIN8

    raise NotImplementedError('Unknown win version %s.' % os_version)

  def CanFlushIndividualFilesFromSystemCache(self):
    return True

  def _GetWin32ProcessInfo(self, func, pid):
    mask = (win32con.PROCESS_QUERY_INFORMATION |
            win32con.PROCESS_VM_READ)
    handle = None
    try:
      handle = win32api.OpenProcess(mask, False, pid)
      return func(handle)
    except pywintypes.error, e:
      errcode = e[0]
      if errcode == 87:
        raise exceptions.ProcessGoneException()
      raise
    finally:
      if handle:
        win32api.CloseHandle(handle)

  def _GetPerformanceInfo(self):
    class PerformanceInfo(ctypes.Structure):
      """Struct for GetPerformanceInfo() call
      http://msdn.microsoft.com/en-us/library/ms683210
      """
      _fields_ = [('size', ctypes.c_ulong),
                  ('CommitTotal', ctypes.c_size_t),
                  ('CommitLimit', ctypes.c_size_t),
                  ('CommitPeak', ctypes.c_size_t),
                  ('PhysicalTotal', ctypes.c_size_t),
                  ('PhysicalAvailable', ctypes.c_size_t),
                  ('SystemCache', ctypes.c_size_t),
                  ('KernelTotal', ctypes.c_size_t),
                  ('KernelPaged', ctypes.c_size_t),
                  ('KernelNonpaged', ctypes.c_size_t),
                  ('PageSize', ctypes.c_size_t),
                  ('HandleCount', ctypes.c_ulong),
                  ('ProcessCount', ctypes.c_ulong),
                  ('ThreadCount', ctypes.c_ulong)]

      def __init__(self):
        self.size = ctypes.sizeof(self)
        super(PerformanceInfo, self).__init__()

    performance_info = PerformanceInfo()
    ctypes.windll.psapi.GetPerformanceInfo(
        ctypes.byref(performance_info), performance_info.size)
    return performance_info

  def LaunchApplication(
      self, application, parameters=None, elevate_privilege=False):
    """Launch an application. Returns a PyHANDLE object."""

    parameters = ' '.join(parameters) if parameters else ''
    if elevate_privilege and not IsCurrentProcessElevated():
      # Use ShellExecuteEx() instead of subprocess.Popen()/CreateProcess() to
      # elevate privileges. A new console will be created if the new process has
      # different permissions than this process.
      proc_info = shell.ShellExecuteEx(
          fMask=shellcon.SEE_MASK_NOCLOSEPROCESS | shellcon.SEE_MASK_NO_CONSOLE,
          lpVerb='runas' if elevate_privilege else '',
          lpFile=application,
          lpParameters=parameters,
          nShow=win32con.SW_HIDE)
      if proc_info['hInstApp'] <= 32:
        raise Exception('Unable to launch %s' % application)
      return proc_info['hProcess']
    else:
      handle, _, _, _ = win32process.CreateProcess(
          None, application + ' ' + parameters, None, None, False,
          win32process.CREATE_NO_WINDOW, None, None, win32process.STARTUPINFO())
      return handle

  def CanMonitorPower(self):
    return self._power_monitor.CanMonitorPower()

  def CanMeasurePerApplicationPower(self):
    return self._power_monitor.CanMeasurePerApplicationPower()

  def StartMonitoringPower(self, browser):
    self._power_monitor.StartMonitoringPower(browser)

  def StopMonitoringPower(self):
    return self._power_monitor.StopMonitoringPower()

  def _StartMsrServerIfNeeded(self):
    if self._msr_server_handle:
      return

    _InstallWinRing0()
    self._msr_server_port = util.GetUnreservedAvailableLocalPort()
    # It might be flaky to get a port number without reserving it atomically,
    # but if the server process chooses a port, we have no way of getting it.
    # The stdout of the elevated process isn't accessible.
    parameters = (
        os.path.join(os.path.dirname(__file__), 'msr_server_win.py'),
        str(self._msr_server_port),
    )
    self._msr_server_handle = self.LaunchApplication(
        sys.executable, parameters, elevate_privilege=True)
    # Wait for server to start. connect has a default timeout of 1 second.
    try:
      socket.create_connection(('127.0.0.1', self._msr_server_port)).close()
    except socket.error:
      self.CloseMsrServer()
    atexit.register(TerminateProcess, self._msr_server_handle)

  def ReadMsr(self, msr_number):
    self._StartMsrServerIfNeeded()
    if not self._msr_server_handle:
      raise OSError('Unable to start MSR server.')

    sock = socket.create_connection(('127.0.0.1', self._msr_server_port), 0.1)
    try:
      sock.sendall(struct.pack('I', msr_number))
      response = sock.recv(8)
    finally:
      sock.close()
    return struct.unpack('Q', response)[0]
