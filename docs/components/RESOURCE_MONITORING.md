# Resource Monitoring System

## Overview

The Resource Monitoring System provides real-time tracking of system resources (CPU, memory, disk) during mission execution in the Jarvis platform. This helps with debugging, optimization, and ensuring missions stay within resource constraints.

## Features

- **System-Wide Monitoring**: Track CPU, memory, and disk usage across the entire system
- **Process-Specific Tracking**: Monitor individual process resource consumption
- **Structured Logging**: All resource metrics are logged in structured JSON format
- **Non-Intrusive**: Monitoring failures don't break mission execution
- **Graceful Degradation**: Works even when resource monitoring is unavailable

## Architecture

### Components

1. **ResourceMonitor**: Static class that provides resource snapshot capabilities
2. **TaskRunner Integration**: Automatic resource logging during mission execution
3. **Structured Logging**: All metrics logged in JSON format for easy parsing

### Metrics Collected

#### System Metrics
- **CPU Percentage**: Current CPU usage (0-100%)
- **Memory Percentage**: Current memory usage (0-100%)
- **Memory Available**: Available memory in MB
- **Disk Percentage**: Current disk usage (0-100%)
- **Disk Free Space**: Free disk space in GB

#### Process Metrics
- **CPU Percentage**: Process CPU usage
- **Memory Usage**: Process memory in MB
- **Thread Count**: Number of threads used by the process

## Usage

### Basic Example

```python
from app.application.services.task_runner import ResourceMonitor

# Get a system resource snapshot
snapshot = ResourceMonitor.get_resource_snapshot()
print(f"CPU: {snapshot['cpu_percent']}%")
print(f"Memory: {snapshot['memory_percent']}%")
print(f"Disk: {snapshot['disk_percent']}%")

# Monitor a specific process
import os
process_resources = ResourceMonitor.get_process_resources(os.getpid())
print(f"Process Memory: {process_resources['memory_mb']} MB")
```

### Integration with TaskRunner

Resource monitoring is automatically enabled in TaskRunner:

```python
from app.application.services.task_runner import TaskRunner
from app.domain.models.mission import Mission

# Create task runner
runner = TaskRunner(device_id="my-device")

# Execute a mission - resources are automatically logged
mission = Mission(
    mission_id="resource-test",
    code="import time; time.sleep(1); print('Done')",
    requirements=[],
    browser_interaction=False,
    keep_alive=False,
)

result = runner.execute_mission(mission, session_id="test-session")

# Resources are logged at:
# - Mission start (initial snapshot)
# - Mission end (final snapshot)
# - During execution (process-specific)
```

## Structured Logging Format

All resource metrics are logged in JSON format:

### Initial Resource Snapshot

```json
{
  "mission_id": "mission_001",
  "device_id": "laptop-001",
  "session_id": "session_123",
  "message": "resources_initial",
  "cpu_percent": 15.2,
  "memory_percent": 42.8,
  "memory_available_mb": 8192.5,
  "disk_percent": 65.3,
  "disk_free_gb": 150.7
}
```

### Final Resource Snapshot

```json
{
  "mission_id": "mission_001",
  "device_id": "laptop-001",
  "session_id": "session_123",
  "message": "resources_final",
  "cpu_percent": 18.7,
  "memory_percent": 45.1,
  "memory_available_mb": 7890.2,
  "disk_percent": 65.3,
  "disk_free_gb": 150.7
}
```

### Process Resource Snapshot

```json
{
  "mission_id": "mission_001",
  "device_id": "laptop-001",
  "session_id": "session_123",
  "message": "process_resources",
  "pid": 12345,
  "cpu_percent": 25.5,
  "memory_mb": 128.3,
  "num_threads": 4
}
```

## Use Cases

### 1. Performance Monitoring

Monitor resource usage to identify performance bottlenecks:

```python
import json

# Parse logs to find resource-intensive missions
with open("jarvis.log") as f:
    for line in f:
        try:
            log = json.loads(line)
            if log.get("message") == "resources_final":
                if log.get("cpu_percent", 0) > 80:
                    print(f"High CPU mission: {log['mission_id']}")
        except:
            pass
```

### 2. Resource Limits

Implement resource-based mission rejection:

```python
def should_execute_mission(mission):
    """Check if system has enough resources for mission"""
    snapshot = ResourceMonitor.get_resource_snapshot()
    
    if snapshot["cpu_percent"] > 90:
        return False, "CPU usage too high"
    
    if snapshot["memory_percent"] > 90:
        return False, "Memory usage too high"
    
    if snapshot["disk_percent"] > 95:
        return False, "Disk space too low"
    
    return True, "OK"
```

### 3. Resource Trending

Track resource usage over time:

```python
import json
from collections import defaultdict

def analyze_resource_trends(log_file):
    """Analyze resource usage trends from logs"""
    trends = defaultdict(list)
    
    with open(log_file) as f:
        for line in f:
            try:
                log = json.loads(line)
                if log.get("message") in ["resources_initial", "resources_final"]:
                    trends["cpu"].append(log.get("cpu_percent", 0))
                    trends["memory"].append(log.get("memory_percent", 0))
            except:
                pass
    
    return {
        "avg_cpu": sum(trends["cpu"]) / len(trends["cpu"]),
        "max_cpu": max(trends["cpu"]),
        "avg_memory": sum(trends["memory"]) / len(trends["memory"]),
        "max_memory": max(trends["memory"]),
    }
```

## Configuration

### Enable/Disable Resource Monitoring

Resource monitoring is always enabled but fails gracefully. To completely disable it, you would need to modify the TaskRunner code.

### Adjust Monitoring Frequency

Currently, resources are monitored:
- Once at mission start
- Once at mission end
- Once during script execution (for process-specific metrics)

To add more frequent monitoring, modify the `_execute_script` method in TaskRunner.

## Best Practices

1. **Parse JSON Logs**: Use proper JSON parsing when analyzing logs
2. **Set Thresholds**: Define resource thresholds appropriate for your hardware
3. **Monitor Trends**: Look for increasing resource usage patterns over time
4. **Correlate with Failures**: Compare resource usage between successful and failed missions
5. **Clean Up Logs**: Regularly rotate and archive resource logs

## Troubleshooting

### Missing Resource Metrics

If resource metrics are missing from logs:

1. **Check psutil installation**: Ensure psutil is installed (`pip install psutil`)
2. **Verify permissions**: Some systems require elevated permissions for full resource monitoring
3. **Check log level**: Ensure logging level is set to INFO or DEBUG

### Inaccurate Metrics

If metrics seem inaccurate:

1. **System load**: High system load can cause measurement variations
2. **Timing**: CPU percentage is measured over a 0.1s interval
3. **Process lifecycle**: Short-lived processes may not be accurately measured

### Performance Impact

Resource monitoring has minimal performance impact:

- System snapshots: ~10-50ms overhead
- Process queries: ~5-20ms overhead
- Total overhead per mission: typically <100ms

To reduce overhead:
- Remove process-specific monitoring if not needed
- Increase measurement intervals
- Disable resource logging in production (modify TaskRunner)

## Metrics Reference

### System Metrics

| Metric | Type | Range | Description |
|--------|------|-------|-------------|
| `cpu_percent` | float | 0-100 | System CPU usage percentage |
| `memory_percent` | float | 0-100 | System memory usage percentage |
| `memory_available_mb` | float | 0+ | Available memory in megabytes |
| `disk_percent` | float | 0-100 | Disk usage percentage |
| `disk_free_gb` | float | 0+ | Free disk space in gigabytes |

### Process Metrics

| Metric | Type | Range | Description |
|--------|------|-------|-------------|
| `cpu_percent` | float | 0+ | Process CPU usage (can exceed 100% on multi-core) |
| `memory_mb` | float | 0+ | Process memory usage in megabytes |
| `num_threads` | int | 1+ | Number of threads in process |

## Dependencies

- **psutil**: Cross-platform library for system and process utilities
  ```bash
  pip install psutil>=5.9.0
  ```

## Related Components

- **TaskRunner**: Main integration point for resource monitoring
- **StructuredLogger**: Handles structured JSON logging
- **Mission**: Missions being monitored for resource usage

## Future Enhancements

- Historical resource tracking database
- Resource usage predictions based on mission type
- Automatic resource limit enforcement
- Resource-based mission scheduling
- Integration with system monitoring tools (Prometheus, Grafana)
- GPU resource monitoring
- Network bandwidth monitoring
- Detailed I/O statistics
