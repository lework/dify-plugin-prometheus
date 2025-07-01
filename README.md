## prometheus

**Author:** lework
**Version:** 0.0.2
**Type:** tool

### Description

## Creating a Dify Plugin

dify plugin init

## Packaging the Plugin

dify plugin package ./prometheus

# Prometheus Query Plugin

A Prometheus query plugin for Dify that allows users to query Prometheus metric data using PromQL.

## Features

- Query Prometheus metric data using PromQL
- Support for time range queries (relative and absolute time)
- Support for basic authentication and token authentication
- Automatic formatting of results for easy understanding
- **Support for Markdown table output**, clearly displaying the latest value of each metric with labels as columns
- **Kubernetes Pod resource metrics query**, getting CPU, memory usage and restart count for Pods

## Configuration

Before using this plugin, you need to configure the following information:

- **API URL**: The URL of the Prometheus server, e.g., `http://localhost:9090`
- **Username/Password**: (Optional) Username and password for basic authentication
- **Token**: (Optional) Bearer token for authentication

## Tools

### 1. Prometheus Query

#### Parameters

- **PromQL Query Statement**: Required, the PromQL query statement to execute
- **Start Time**: Optional, the start time of the query, supports the following formats:
  - RFC3339/ISO8601 format: `2023-01-01T00:00:00Z`
  - Relative time: `1h`, `2d`, `3w`, `4m`, `5y`, etc.
  - Default value: `1h` (1 hour ago)
- **End Time**: Optional, the end time of the query, supports the same formats as the start time
  - Default value: `now` (current time)
- **Step**: Optional, the resolution step of the query
  - Format: `15s`, `1m`, `1h`, etc.
  - Default value: `15s` (15 seconds)

#### Examples

##### Query CPU Usage

```
query: 100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
start_time: 1h
end_time: now
step: 1m
```

##### Query Memory Usage

```
query: 100 * (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes))
start_time: 12h
end_time: now
step: 5m
```

### 2. Kubernetes Pod Resource Metrics Query

Get resource usage information for Kubernetes Pods, including CPU, memory usage and restart count, displayed in Markdown table format.

#### Parameters

- **Namespace**: Optional, Kubernetes namespace name, if not specified, queries all namespaces
- **Label Selector**: Optional, label selector to filter Pods, e.g., `app=myapp,component=database`
- **Pod Name Pattern**: Optional, regular expression to filter Pod names, e.g., `frontend-.*`

#### Examples

##### Query Pod Resource Usage in a Specific Namespace

```
namespace: default
```

##### Query Pod Resource Usage for a Specific Application

```
selector: app=myapp
```

##### Query Pod Resource Usage with a Specific Prefix

```
pod_name_pattern: frontend-.*
```

#### Return Result

Returns a Markdown table containing the following information:

| Pod Name | Age      | Namespace | Node  | Ready | Phase   | CPU Usage % | Memory Usage MiB | CPU Request | CPU Limit | Memory Request MiB | Memory Limit MiB | Restarts in 24h |
| -------- | -------- | --------- | ----- | ----- | ------- | ----------- | ---------------- | ----------- | --------- | ------------------ | ---------------- | --------------- |
| pod-1    | 1.0 day  | default   | node1 | ✓     | Running | 0.819%      | 500 MiB          | 0.100       | 1         | 500 MiB            | 2 GiB            | 0               |
| pod-2    | 1.7 days | default   | node2 | ✓     | Running | 0.380%      | 256 MiB          | 0.100       | 1         | 256 MiB            | 2 GiB            | 0               |

## Return Results

### Markdown Table Format (New Feature)

For matrix type query results, the plugin will generate a Markdown table, **using labels as table columns**, making it easier to clearly display the data:

```markdown
### node_cpu_seconds_total

| timestamp           | instance       | job        | mode   | value |
| :------------------ | :------------- | :--------- | :----- | ----: |
| 2023-03-11T18:15:00 | 10.131.242.148 | prometheus | idle   | 0.278 |
| 2023-03-11T18:15:00 | 10.131.242.149 | prometheus | system | 0.156 |

_Showing the most recent data points_
```

### JSON Format

When a Markdown table cannot be generated, the plugin will return the complete result in JSON format:

```json
{
  "success": true,
  "result_type": "matrix",
  "data": [
    {
      "metric": "metric_name",
      "labels": {
        "instance": "localhost:9090",
        "job": "prometheus"
      },
      "values": [
        {
          "timestamp": "2023-01-01T00:00:00.000000",
          "value": 12.34
        },
        ...
      ]
    },
    ...
  ]
}
```
