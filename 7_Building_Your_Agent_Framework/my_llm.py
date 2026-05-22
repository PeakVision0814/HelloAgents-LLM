# 7_Building_Your_Agent_Framework\my_llm.py
import os
from typing import Optional
from openai import OpenAI
from hello_agents import HelloAgentsException, HelloAgentsLLM


class MyLLM(HelloAgentsLLM):
    """
    一个自定义的 LLM 客户端，通过继承增加了对 ModelScope 的支持。
    """

    def __init__(
        self,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        provider: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        timeout: Optional[int] = None,
        **kwargs,
    ):
        # 仅在 provider=modelscope 时走自定义初始化逻辑；
        # 其他 provider 全部回退到父类，保持 OpenAI 等内置供应商可用。
        if provider != "modelscope":
            super().__init__(
                model=model,
                api_key=api_key,
                base_url=base_url,
                provider=provider,
                temperature=temperature,
                max_tokens=max_tokens,
                timeout=timeout,
                **kwargs,
            )
            return

        self.provider = "modelscope"
        self.model = (
            model
            or os.getenv("MODELSCOPE_MODEL_ID")
            or os.getenv("LLM_MODEL_ID")
            or "Qwen/Qwen2.5-72B-Instruct"
        )
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout or int(os.getenv("LLM_TIMEOUT", "60"))
        self.kwargs = kwargs

        self.api_key = api_key or os.getenv("MODELSCOPE_API_KEY") or os.getenv("LLM_API_KEY")
        self.base_url = (
            base_url
            or os.getenv("MODELSCOPE_BASE_URL")
            or os.getenv("LLM_BASE_URL")
            or "https://api-inference.modelscope.cn/v1/"
        )

        if not self.api_key:
            raise HelloAgentsException(
                "ModelScope API key 未提供，请设置 MODELSCOPE_API_KEY 或 LLM_API_KEY。"
            )

        self._client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=self.timeout,
        )

# class MyLLM(HelloAgentsLLM):
#     def __init__(
#         self,
#         model: Optional[str] = None,
#         api_key: Optional[str] = None,
#         base_url: Optional[str] = None,
#         provider: Optional[str] = "auto",
#         **kwargs
#     ):
#         # 检查provider是否为我们想处理的'modelscope'
#         if provider == "modelscope":
#             print("正在使用自定义的 ModelScope Provider")
#             self.provider = "modelscope"
            
#             # 解析 ModelScope 的凭证
#             self.api_key = api_key or os.getenv("MODELSCOPE_API_KEY")
#             self.base_url = base_url or "https://api-inference.modelscope.cn/v1/"
            
#             # 验证凭证是否存在
#             if not self.api_key:
#                 raise ValueError("ModelScope API key not found. Please set MODELSCOPE_API_KEY environment variable.")

#             # 设置默认模型和其他参数
#             self.model = model or os.getenv("LLM_MODEL_ID") or "Qwen/Qwen2.5-VL-72B-Instruct"
#             self.temperature = kwargs.get('temperature', 0.7)
#             self.max_tokens = kwargs.get('max_tokens')
#             self.timeout = kwargs.get('timeout', 60)
            
#             # 使用获取的参数创建OpenAI客户端实例
#             self._client = OpenAI(api_key=self.api_key, base_url=self.base_url, timeout=self.timeout)

#         else:
#             # 如果不是 modelscope, 则完全使用父类的原始逻辑来处理
#             super().__init__(model=model, api_key=api_key, base_url=base_url, provider=provider, **kwargs)
