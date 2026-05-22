import os
import sys
from pathlib import Path
from typing import Optional

try:
    from hello_agents import HelloAgentsException, HelloAgentsLLM
except ModuleNotFoundError:
    # 回退到核心模块直导，避免 hello_agents 包根导入时拉起额外评测依赖。
    HELLO_AGENTS_DIR = Path(__file__).resolve().parent / "hello_agents"
    if str(HELLO_AGENTS_DIR) not in sys.path:
        sys.path.insert(0, str(HELLO_AGENTS_DIR))

    from core.exceptions import HelloAgentsException
    from core.llm import HelloAgentsLLM


class MyGeminiLLM(HelloAgentsLLM):
    """
    通过继承为 HelloAgentsLLM 增加 Gemini 提供商支持。

    设计目标：
    1. 继续复用父类已有的 OpenAI 兼容调用流程
    2. 支持显式 provider="gemini"
    3. 支持根据 Gemini 专用环境变量自动识别
    """

    DEFAULT_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
    DEFAULT_MODEL = "gemini-3.5-flash"

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
        normalized_provider = provider.lower() if isinstance(provider, str) else provider
        super().__init__(
            model=model,
            api_key=api_key,
            base_url=base_url,
            provider=normalized_provider,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=timeout,
            **kwargs,
        )

        # 父类会优先读取通用 LLM_MODEL_ID，这里为 Gemini 补回专用模型优先级。
        if str(self.provider).lower() == "gemini" and model is None:
            self.model = (
                os.getenv("GEMINI_MODEL_ID")
                or os.getenv("GOOGLE_MODEL_ID")
                or self.model
                or self.DEFAULT_MODEL
            )

    def _auto_detect_provider(self, api_key: Optional[str], base_url: Optional[str]) -> str:
        """优先检测 Gemini，再回退到父类的自动检测逻辑。"""
        if (
            os.getenv("GEMINI_API_KEY")
            or os.getenv("GOOGLE_API_KEY")
            or os.getenv("GEMINI_BASE_URL")
            or os.getenv("GOOGLE_BASE_URL")
        ):
            return "gemini"

        actual_api_key = api_key or os.getenv("LLM_API_KEY")
        if actual_api_key and actual_api_key.startswith("AIza"):
            return "gemini"

        actual_base_url = base_url or os.getenv("LLM_BASE_URL")
        if actual_base_url and "generativelanguage.googleapis.com" in actual_base_url.lower():
            return "gemini"

        return super()._auto_detect_provider(api_key, base_url)

    def _resolve_credentials(self, api_key: Optional[str], base_url: Optional[str]) -> tuple[str, str]:
        """为 Gemini 解析专用环境变量，其余 provider 继续使用父类逻辑。"""
        if str(self.provider).lower() != "gemini":
            return super()._resolve_credentials(api_key, base_url)

        resolved_api_key = (
            api_key
            or os.getenv("GEMINI_API_KEY")
            or os.getenv("GOOGLE_API_KEY")
            or os.getenv("LLM_API_KEY")
        )
        resolved_base_url = (
            base_url
            or os.getenv("GEMINI_BASE_URL")
            or os.getenv("GOOGLE_BASE_URL")
            or os.getenv("LLM_BASE_URL")
            or self.DEFAULT_BASE_URL
        )

        if not resolved_api_key:
            raise HelloAgentsException(
                "Gemini API key 未提供，请设置 GEMINI_API_KEY、GOOGLE_API_KEY 或 LLM_API_KEY。"
            )

        return resolved_api_key, resolved_base_url

    def _get_default_model(self) -> str:
        """为 Gemini 提供更合适的默认模型。"""
        if str(self.provider).lower() != "gemini":
            return super()._get_default_model()

        return (
            os.getenv("GEMINI_MODEL_ID")
            or os.getenv("GOOGLE_MODEL_ID")
            or os.getenv("LLM_MODEL_ID")
            or self.DEFAULT_MODEL
        )
