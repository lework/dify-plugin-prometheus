## prometheus

**Author:** lework
**Version:** 0.0.1
**Type:** tool

### Description

## 创建 Dify 插件

dify plugin init

## 打包插件

dify plugin package ./prometheus

# Prometheus 查询插件

Dify 的 Prometheus 查询插件，允许用户通过 PromQL 查询 Prometheus 指标数据。

## 功能

- 使用 PromQL 查询 Prometheus 指标数据
- 支持时间范围查询（相对时间和绝对时间）
- 支持基本认证和令牌认证
- 自动格式化结果以便于理解
- **支持 Markdown 表格输出**，将标签作为列清晰展示每个指标的最新值
- **Kubernetes Pod 资源指标查询**，获取 Pod 的 CPU、内存使用情况和重启次数

## 配置

在使用此插件前，需要配置以下信息：

- **API URL**: Prometheus 服务器的 URL，例如 `http://localhost:9090`
- **用户名/密码**: (可选) 基本认证的用户名和密码
- **令牌**: (可选) Bearer 令牌认证

## 工具

### 1. Prometheus 查询

#### 参数

- **PromQL 查询语句**: 必填，要执行的 PromQL 查询语句
- **开始时间**: 可选，查询的开始时间，支持以下格式：
  - RFC3339/ISO8601 格式: `2023-01-01T00:00:00Z`
  - 相对时间: `1h`, `2d`, `3w`, `4m`, `5y` 等
  - 默认值: `1h` (1 小时前)
- **结束时间**: 可选，查询的结束时间，支持与开始时间相同的格式
  - 默认值: `now` (当前时间)
- **步长**: 可选，查询分辨率步长
  - 格式: `15s`, `1m`, `1h` 等
  - 默认值: `15s` (15 秒)

#### 示例

##### 查询 CPU 使用率

```
query: 100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
start_time: 1h
end_time: now
step: 1m
```

##### 查询内存使用率

```
query: 100 * (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes))
start_time: 12h
end_time: now
step: 5m
```

### 2. Kubernetes Pod 资源指标查询

获取 Kubernetes Pod 的资源使用情况，包括 CPU、内存使用率以及重启次数等信息，并以 Markdown 表格的形式展示。

#### 参数

- **命名空间**: 可选，Kubernetes 命名空间名称，不填则查询所有命名空间
- **标签选择器**: 可选，用于过滤 Pod 的标签选择器，例如 `app=myapp,component=database`
- **Pod 名称模式**: 可选，用于过滤 Pod 名称的正则表达式，例如 `frontend-.*`

#### 示例

##### 查询特定命名空间的 Pod 资源使用情况

```
namespace: default
```

##### 查询特定应用的 Pod 资源使用情况

```
selector: app=myapp
```

##### 查询特定前缀的 Pod 资源使用情况

```
pod_name_pattern: frontend-.*
```

#### 返回结果

返回包含以下信息的 Markdown 表格：

| Pod 名称 | 存活时长 | 命名空间 | 节点  | 就绪状态 | Phase   | CPU 使用% | 内存使用 MiB | CPU 请求 | CPU 限制 | 内存请求 MiB | 内存限制 MiB | 24h 重启次数 |
| -------- | -------- | -------- | ----- | -------- | ------- | --------- | ------------ | -------- | -------- | ------------ | ------------ | ------------ |
| pod-1    | 1.0 天   | default  | node1 | ✓        | Running | 0.819%    | 500 MiB      | 0.100    | 1        | 500 MiB      | 2 GiB        | 0            |
| pod-2    | 1.7 天   | default  | node2 | ✓        | Running | 0.380%    | 256 MiB      | 0.100    | 1        | 256 MiB      | 2 GiB        | 0            |

## 返回结果

### Markdown 表格格式 (新增特性)

对于矩阵类型的查询结果，插件会生成 Markdown 表格，**将标签作为表格列**，便于清晰展示数据：

```markdown
### node_cpu_seconds_total

| timestamp           | instance       | job        | mode   | value |
| :------------------ | :------------- | :--------- | :----- | ----: |
| 2023-03-11T18:15:00 | 10.131.242.148 | prometheus | idle   | 0.278 |
| 2023-03-11T18:15:00 | 10.131.242.149 | prometheus | system | 0.156 |

_显示最近的数据点_
```

### JSON 格式

当无法生成 Markdown 表格时，插件会返回 JSON 格式的完整结果：

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
