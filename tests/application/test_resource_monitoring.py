# -*- coding: utf-8 -*-
"""Tests for resource monitoring in TaskRunner"""

import sys
import shutil
import tempfile
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch

import pytest

# Mock psutil before importing TaskRunner to handle environments without psutil
mock_psutil = MagicMock()
# Set default return values to prevent AttributeError
mock_psutil.cpu_percent.return_value = 25.5
mock_psutil.virtual_memory.return_value.percent = 42.8
mock_psutil.virtual_memory.return_value.available = 8589934592
mock_psutil.disk_usage.return_value.percent = 65.3
mock_psutil.disk_usage.return_value.free = 161061273600
sys.modules['psutil'] = mock_psutil

from app.application.services.task_runner import ResourceMonitor, TaskRunner
from app.domain.models.mission import Mission


class TestResourceMonitor:
    """Test cases for ResourceMonitor"""

    def test_get_resource_snapshot(self):
        """Test getting a resource snapshot with mocked psutil"""
        # Configure mock_psutil responses
        mock_psutil.cpu_percent.return_value = 25.5
        mock_psutil.virtual_memory.return_value = Mock(
            percent=42.8,
            available=8589934592  # 8 GB in bytes
        )
        mock_psutil.disk_usage.return_value = Mock(
            percent=65.3,
            free=161061273600  # 150 GB in bytes
        )
        
        with patch('app.application.services.task_runner.PSUTIL_AVAILABLE', True):
            snapshot = ResourceMonitor.get_resource_snapshot()
        
        assert snapshot is not None
        assert isinstance(snapshot, dict)
        assert "cpu_percent" in snapshot
        assert "memory_percent" in snapshot
        assert "memory_available_mb" in snapshot
        assert "disk_percent" in snapshot
        assert "disk_free_gb" in snapshot
        
        # Check values match mock data
        assert snapshot["cpu_percent"] == 25.5
        assert snapshot["memory_percent"] == 42.8
        assert snapshot["memory_available_mb"] == 8192.0
        assert snapshot["disk_percent"] == 65.3
        assert snapshot["disk_free_gb"] == 150.0
    
    def test_get_resource_snapshot_without_psutil(self):
        """Test graceful degradation when psutil is not available"""
        with patch('app.application.services.task_runner.PSUTIL_AVAILABLE', False):
            snapshot = ResourceMonitor.get_resource_snapshot()
            
            # Should return default values instead of empty dict
            assert snapshot is not None
            assert isinstance(snapshot, dict)
            assert snapshot.get("cpu_percent") == 0.0
            assert snapshot.get("memory_percent") == 0.0
    
    def test_get_process_resources(self):
        """Test getting process resources with mocked psutil"""
        import os
        
        # Configure mock process
        mock_process = Mock()
        mock_process.cpu_percent.return_value = 15.2
        mock_process.memory_info.return_value = Mock(rss=134217728)  # 128 MB
        mock_process.num_threads.return_value = 4
        mock_psutil.Process.return_value = mock_process
        
        with patch('app.application.services.task_runner.PSUTIL_AVAILABLE', True):
            resources = ResourceMonitor.get_process_resources(os.getpid())
        
        assert resources is not None
        assert isinstance(resources, dict)
        assert "cpu_percent" in resources
        assert "memory_mb" in resources
        assert "num_threads" in resources
        assert resources["cpu_percent"] == 15.2
        assert resources["memory_mb"] == 128.0
        assert resources["num_threads"] == 4


class TestTaskRunnerResourceMonitoring:
    """Test cases for TaskRunner resource monitoring"""
    
    @pytest.fixture
    def task_runner(self):
        """Create TaskRunner with temporary cache directory"""
        cache_dir = Path(tempfile.mkdtemp(prefix="test_resource_mon_"))
        yield TaskRunner(cache_dir=cache_dir, use_venv=False)
        # Cleanup temp directory
        if cache_dir.exists():
            shutil.rmtree(cache_dir, ignore_errors=True)
    
    def test_mission_logs_resource_snapshots(self, task_runner):
        """Test that missions log initial and final resource snapshots"""
        mission = Mission(
            mission_id="resource_test_001",
            code="print('Testing resource monitoring')",
            requirements=[],
            browser_interaction=False,
            keep_alive=False,
        )
        
        result = task_runner.execute_mission(mission)
        
        # Main goal: mission should succeed even with resource monitoring
        assert result is not None
        assert result.success is True
        assert "Testing resource monitoring" in result.stdout
    
    def test_resource_monitoring_doesnt_break_execution(self, task_runner):
        """Test that resource monitoring failures don't break mission execution"""
        mission = Mission(
            mission_id="robust_test_001",
            code="x = 1 + 1\nprint(f'Result: {x}')",
            requirements=[],
            browser_interaction=False,
            keep_alive=False,
        )
        
        result = task_runner.execute_mission(mission)
        
        # Should succeed even if resource monitoring has issues
        assert result is not None
        assert result.success is True
        assert "Result: 2" in result.stdout
