from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError
import requests


class PrometheusProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            # 验证必要的凭证字段是否存在
            if "api_url" not in credentials:
                raise ValueError("Prometheus API URL必须提供")
            
            # 尝试连接Prometheus服务器
            api_url = credentials["api_url"]
            headers = {}
            
            # 如果提供了认证信息，则添加到请求头中
            if "username" in credentials and "password" in credentials:
                import base64
                auth_str = f"{credentials['username']}:{credentials['password']}"
                auth_bytes = auth_str.encode('ascii')
                base64_bytes = base64.b64encode(auth_bytes)
                base64_auth = base64_bytes.decode('ascii')
                headers["Authorization"] = f"Basic {base64_auth}"
            
            # 如果提供了令牌，则添加到请求头中
            if "token" in credentials:
                headers["Authorization"] = f"Bearer {credentials['token']}"
            
            # 测试连接
            response = requests.get(
                f"{api_url}/api/v1/metadata", 
                headers=headers,
                timeout=10
            )
            
            # 检查响应
            if response.status_code != 200:
                raise ValueError(f"无法连接到Prometheus服务器: HTTP {response.status_code}")
            
            # 检查是否有Kubernetes相关指标
            # 对于Kubernetes Pod Metrics工具，我们需要验证是否存在必要的Kubernetes指标
            k8s_metrics_response = requests.get(
                f"{api_url}/api/v1/query",
                params={"query": "kube_pod_info"},
                headers=headers,
                timeout=10
            )
            
            # 如果k8s_metrics_response.status_code不等于200或者结果为空，则输出警告但不阻止凭证验证
            if k8s_metrics_response.status_code != 200 or not k8s_metrics_response.json().get("data", {}).get("result", []):
                print("警告: 未找到Kubernetes指标，Kubernetes Pod Metrics工具可能无法正常工作")
            
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
