# Copyright (c) 2013 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

{
  'variables': {
    'tracing_template_files': [
      'src/about_tracing.html.template',
      'src/about_tracing.js.template',
    ],
    'tracing_html_files': [
      'src/tracing/record_selection_dialog.html',
      'src/tracing/timeline_view.html',
      'src/tracing/category_filter_dialog.html',
      'src/tracing/analysis/cpu_slice_view.html',
      'src/tracing/analysis/thread_time_slice_view.html',
      'src/tracing/find_control.html',
      'src/ui/mouse_mode_selector.html',
      'src/ui/overlay.html',
      'src/ui/quad_stack_view.html',
      'src/cc/picture_debugger.html',
    ],
    'tracing_css_files': [
      'src/base/unittest.css',
      'src/about_tracing/tracing_controller.css',
      'src/about_tracing/profiling_view.css',
      'src/ui/info_bar.css',
      'src/ui/list_view.css',
      'src/ui/tool_button.css',
      'src/ui/mouse_mode_selector.css',
      'src/ui/list_and_associated_view.css',
      'src/ui/drag_handle.css',
      'src/ui/trace_viewer.css',
      'src/ui/quad_stack_view.css',
      'src/system_stats/system_stats_snapshot_view.css',
      'src/tcmalloc/tcmalloc_instance_view.css',
      'src/tcmalloc/tcmalloc_snapshot_view.css',
      'src/tcmalloc/heap_instance_track.css',
      'src/tracing/analysis/analyze_slices.css',
      'src/tracing/analysis/default_object_view.css',
      'src/tracing/analysis/analysis_results.css',
      'src/tracing/analysis/analysis_view.css',
      'src/tracing/analysis/analysis_link.css',
      'src/tracing/analysis/generic_object_view.css',
      'src/tracing/timeline_view.css',
      'src/tracing/tracks/ruler_track.css',
      'src/tracing/tracks/counter_track.css',
      'src/tracing/tracks/thread_track.css',
      'src/tracing/tracks/process_track_base.css',
      'src/tracing/tracks/trace_model_track.css',
      'src/tracing/tracks/track.css',
      'src/tracing/tracks/heading_track.css',
      'src/tracing/tracks/drawing_container.css',
      'src/tracing/tracks/object_instance_track.css',
      'src/tracing/tracks/slice_track.css',
      'src/tracing/tracks/spacing_track.css',
      'src/tracing/timeline_track_view.css',
      'src/tracing/record_selection_dialog.css',
      'src/cc/layer_picker.css',
      'src/cc/layer_tree_quad_stack_view.css',
      'src/cc/raster_task_slice_view.css',
      'src/cc/picture_view.css',
      'src/cc/picture_ops_list_view.css',
      'src/cc/picture_ops_chart_view.css',
      'src/cc/picture_ops_chart_summary_view.css',
      'src/cc/layer_view.css',
      'src/cc/layer_tree_host_impl_view.css',
      'src/cc/picture_debugger.css',
    ],
    'tracing_js_files': [
      'src/base.js',
      'src/cc.js',
      'src/base/unittest.js',
      'src/base/range.js',
      'src/base/raf.js',
      'src/base/gl_matrix.js',
      'src/base/key_event_manager.js',
      'src/base/rect.js',
      'src/base/settings.js',
      'src/base/quad.js',
      'src/base/unittest/test_error.js',
      'src/base/unittest/assertions.js',
      'src/base/utils.js',
      'src/base/properties.js',
      'src/base/sorted_array_utils.js',
      'src/base/bbox2.js',
      'src/base/measuring_stick.js',
      'src/base/guid.js',
      'src/base/events.js',
      'src/base/color.js',
      'src/base/event_target.js',
      'src/base/iteration_helpers.js',
      'src/base/interval_tree.js',
      'src/about_tracing/profiling_view.js',
      'src/about_tracing/tracing_controller.js',
      'src/ui.js',
      'src/ui/container_that_decorates_its_children.js',
      'src/ui/info_bar.js',
      'src/ui/list_and_associated_view.js',
      'src/ui/camera.js',
      'src/ui/animation.js',
      'src/ui/animation_controller.js',
      'src/ui/overlay.js',
      'src/ui/drag_handle.js',
      'src/ui/list_view.js',
      'src/ui/mouse_mode_selector.js',
      'src/ui/mouse_tracker.js',
      'src/ui/quad_view.js',
      'src/ui/quad_stack_view.js',
      'src/ui/dom_helpers.js',
      'src/system_stats/system_stats_snapshot.js',
      'src/system_stats/system_stats_snapshot_view.js',
      'src/tcmalloc/heap_instance_track.js',
      'src/tcmalloc/tcmalloc_instance_view.js',
      'src/tcmalloc/heap.js',
      'src/tcmalloc/tcmalloc_snapshot_view.js',
      'src/tracing/constants.js',
      'src/tracing/category_filter_dialog.js',
      'src/tracing/record_selection_dialog.js',
      'src/tracing/standalone_timeline_view.js',
      'src/tracing/importer.js',
      'src/tracing/timing_tool.js',
      'src/tracing/trace_model.js',
      'src/tracing/trace_model_settings.js',
      'src/tracing/trace_model/process_base.js',
      'src/tracing/trace_model/cpu.js',
      'src/tracing/trace_model/event.js',
      'src/tracing/trace_model/timed_event.js',
      'src/tracing/trace_model/time_to_object_instance_map.js',
      'src/tracing/trace_model/async_slice.js',
      'src/tracing/trace_model/async_slice_group.js',
      'src/tracing/trace_model/slice_group.js',
      'src/tracing/trace_model/flow_event.js',
      'src/tracing/trace_model/thread.js',
      'src/tracing/trace_model/object_snapshot.js',
      'src/tracing/trace_model/sample.js',
      'src/tracing/trace_model/kernel.js',
      'src/tracing/trace_model/slice.js',
      'src/tracing/trace_model/object_collection.js',
      'src/tracing/trace_model/object_instance.js',
      'src/tracing/trace_model/process.js',
      'src/tracing/trace_model/counter.js',
      'src/tracing/trace_model/counter_sample.js',
      'src/tracing/trace_model/counter_series.js',
      'src/tracing/trace_model/instant_event.js',
      'src/tracing/test_utils.js',
      'src/tracing/timeline_viewport.js',
      'src/tracing/timeline_display_transform.js',
      'src/tracing/timeline_display_transform_animations.js',
      'src/tracing/analysis/stub_analysis_table.js',
      'src/tracing/analysis/object_instance_view.js',
      'src/tracing/analysis/analysis_link.js',
      'src/tracing/analysis/analysis_results.js',
      'src/tracing/analysis/cpu_slice_view.js',
      'src/tracing/analysis/thread_time_slice_view.js',
      'src/tracing/analysis/util.js',
      'src/tracing/analysis/slice_view.js',
      'src/tracing/analysis/generic_object_view.js',
      'src/tracing/analysis/analyze_selection.js',
      'src/tracing/analysis/stub_analysis_results.js',
      'src/tracing/analysis/default_object_view.js',
      'src/tracing/analysis/analyze_counters.js',
      'src/tracing/analysis/analyze_slices.js',
      'src/tracing/analysis/analysis_view.js',
      'src/tracing/analysis/object_snapshot_view.js',
      'src/tracing/timeline_view.js',
      'src/tracing/tracks/counter_track.js',
      'src/tracing/tracks/cpu_track.js',
      'src/tracing/tracks/slice_track.js',
      'src/tracing/tracks/container_track.js',
      'src/tracing/tracks/async_slice_group_track.js',
      'src/tracing/tracks/ruler_track.js',
      'src/tracing/tracks/heading_track.js',
      'src/tracing/tracks/drawing_container.js',
      'src/tracing/tracks/object_instance_track.js',
      'src/tracing/tracks/thread_track.js',
      'src/tracing/tracks/process_track.js',
      'src/tracing/tracks/process_track_base.js',
      'src/tracing/tracks/slice_group_track.js',
      'src/tracing/tracks/spacing_track.js',
      'src/tracing/tracks/kernel_track.js',
      'src/tracing/tracks/track.js',
      'src/tracing/tracks/trace_model_track.js',
      'src/tracing/find_control.js',
      'src/tracing/fast_rect_renderer.js',
      'src/tracing/color_scheme.js',
      'src/tracing/filter.js',
      'src/tracing/importer/gzip_importer.js',
      'src/tracing/importer/zip_importer.js',
      'src/tracing/importer/importer.js',
      'src/tracing/importer/v8/codemap.js',
      'src/tracing/importer/v8/log_reader.js',
      'src/tracing/importer/v8/splaytree.js',
      'src/tracing/importer/v8_log_importer.js',
      'src/tracing/importer/timeline_stream_importer.js',
      'src/tracing/importer/linux_perf/clock_parser.js',
      'src/tracing/importer/linux_perf/exynos_parser.js',
      'src/tracing/importer/linux_perf/workqueue_parser.js',
      'src/tracing/importer/linux_perf/gesture_parser.js',
      'src/tracing/importer/linux_perf/power_parser.js',
      'src/tracing/importer/linux_perf/disk_parser.js',
      'src/tracing/importer/linux_perf/i915_parser.js',
      'src/tracing/importer/linux_perf/cpufreq_parser.js',
      'src/tracing/importer/linux_perf/bus_parser.js',
      'src/tracing/importer/linux_perf/kfunc_parser.js',
      'src/tracing/importer/linux_perf/parser.js',
      'src/tracing/importer/linux_perf/drm_parser.js',
      'src/tracing/importer/linux_perf/sched_parser.js',
      'src/tracing/importer/linux_perf/sync_parser.js',
      'src/tracing/importer/linux_perf/mali_parser.js',
      'src/tracing/importer/linux_perf/android_parser.js',
      'src/tracing/importer/linux_perf_importer.js',
      'src/tracing/importer/trace_event_importer.js',
      'src/tracing/timeline_track_view.js',
      'src/tracing/selection.js',
      'src/tracing/draw_helpers.js',
      'src/tracing/elided_cache.js',
      'src/system_stats.js',
      'src/tcmalloc.js',
      'src/cc/debug_colors.js',
      'src/cc/picture.js',
      'src/cc/picture_as_image_data.js',
      'src/cc/constants.js',
      'src/cc/layer_view.js',
      'src/cc/picture_view.js',
      'src/cc/tile.js',
      'src/cc/region.js',
      'src/cc/layer_impl.js',
      'src/cc/picture_ops_list_view.js',
      'src/cc/picture_ops_chart_view.js',
      'src/cc/picture_ops_chart_summary_view.js',
      'src/cc/util.js',
      'src/cc/layer_picker.js',
      'src/cc/layer_tree_host_impl.js',
      'src/cc/layer_tree_quad_stack_view.js',
      'src/cc/layer_tree_impl.js',
      'src/cc/raster_task_slice_view.js',
      'src/cc/picture_debugger.js',
      'src/cc/layer_tree_host_impl_view.js',
      'src/cc/tile_coverage_rect.js',
      'src/cc/tile_view.js',
      'src/cc/selection.js',
    ],
    'tracing_img_files': [
      'src/images/chrome-left.png',
      'src/images/chrome-right.png',
      'src/images/chrome-mid.png',
      'src/images/collapse.png',
      'src/images/expand.png',
      'src/images/ui-states.png',
    ],
    'tracing_files': [
      '<@(tracing_template_files)',
      '<@(tracing_html_files)',
      '<@(tracing_css_files)',
      '<@(tracing_js_files)',
      '<@(tracing_img_files)',
    ],
  },
  'targets': [
    {
      'target_name': 'generate_about_tracing',
      'type': 'none',
      'actions': [
        {
          'action_name': 'generate_about_tracing',
          'script_name': 'build/generate_about_tracing_contents.py',
          'inputs': [
            '<@(tracing_files)',
          ],
          'outputs': [
            '<(SHARED_INTERMEDIATE_DIR)/content/browser/tracing/about_tracing.js',
            '<(SHARED_INTERMEDIATE_DIR)/content/browser/tracing/about_tracing.html'
          ],
          'action': ['python', '<@(_script_name)',
                     '--outdir', '<(SHARED_INTERMEDIATE_DIR)/content/browser/tracing']
        }
      ]
    }
  ]
}
