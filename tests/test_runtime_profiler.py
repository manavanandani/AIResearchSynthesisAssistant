"""Tests for runtime profiler and efficiency metrics."""

import time
from src.benchmark.runtime_profiler import RuntimeProfiler


def test_runtime_profiler_efficiency():
    def dummy_task():
        time.sleep(0.01)
        return "completed"

    res, profile = RuntimeProfiler.profile(sample_count=100, execution_fn=dummy_task)
    assert res == "completed"
    assert profile.sample_size == 100
    assert profile.pipeline_synthesis_minutes <= 15.0
    assert profile.efficiency_gain_factor > 10.0
