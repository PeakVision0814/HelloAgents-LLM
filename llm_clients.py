import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI


PROJECT_ROOT = Path(__file__).resolve().parent
ENV_PATH = PROJECT_ROOT / ".env"


def load_project_env(override: bool = False) -> None:
    """Load the project-level .env once for all examples."""
    load_dotenv(ENV_PATH, override=override)


load_project_env()


def get_env(name: str, default: str | None = None) -> str | None:
    return os.getenv(name, default)


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"未读取到 {name}，请先检查 {ENV_PATH} 或系统环境变量。")
    return value


@dataclass(frozen=True)
class LLMConfig:
    model: str
    api_key: str
    base_url: str
    timeout: int


def get_llm_config(
    *,
    default_model: str = "gpt-4o-mini",
    model: str | None = None,
    api_key: str | None = None,
    base_url: str | None = None,
    timeout: int | None = None,
) -> LLMConfig:
    load_project_env()

    resolved_api_key = api_key or os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not resolved_api_key:
        raise ValueError(f"未读取到 LLM_API_KEY，请先检查 {ENV_PATH} 或系统环境变量。")

    return LLMConfig(
        model=model or os.getenv("LLM_MODEL_ID", default_model),
        api_key=resolved_api_key,
        base_url=base_url or os.getenv("LLM_BASE_URL", "https://api.openai.com/v1"),
        timeout=timeout or int(os.getenv("LLM_TIMEOUT", 60)),
    )


class HelloAgentsLLM:
    """
    Shared OpenAI-compatible client for the teaching examples.

    It keeps the original `think` interface used in Chapter 4 and also offers
    `generate` for simpler single-prompt examples.
    """

    def __init__(
        self,
        model: str | None = None,
        apiKey: str | None = None,
        baseUrl: str | None = None,
        timeout: int | None = None,
        api_key: str | None = None,
        base_url: str | None = None,
        default_model: str = "gpt-4o-mini",
    ):
        config = get_llm_config(
            default_model=default_model,
            model=model,
            api_key=api_key or apiKey,
            base_url=base_url or baseUrl,
            timeout=timeout,
        )
        self.model = config.model
        self.client = OpenAI(
            api_key=config.api_key,
            base_url=config.base_url,
            timeout=config.timeout,
        )

    @staticmethod
    def _strip_thinking(text: str) -> str:
        return re.sub(r"<think>.*?</think>\s*", "", text, flags=re.DOTALL)

    def generate(self, prompt: str, system_prompt: str, temperature: float = 0) -> str:
        """Call the model once and return the full answer."""
        print("正在调用大语言模型...")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                temperature=temperature,
                stream=False,
            )
            answer = response.choices[0].message.content or ""
            print("大语言模型响应成功。")
            return self._strip_thinking(answer)
        except Exception as error:
            print(f"调用LLM API时发生错误: {error}")
            return "错误:调用语言模型服务时出错。"

    def think(self, messages: list[dict[str, str]], temperature: float = 0) -> str | None:
        """Stream a chat completion and return the collected text."""
        print(f"正在调用 {self.model} 模型...")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                stream=True,
            )

            print("大语言模型响应成功:")
            collected_content = []
            for chunk in response:
                if not chunk.choices:
                    continue
                content = chunk.choices[0].delta.content or ""
                print(content, end="", flush=True)
                collected_content.append(content)
            print()
            return self._strip_thinking("".join(collected_content))
        except Exception as error:
            print(f"调用LLM API时发生错误: {error}")
            return None


def create_chat_openai(temperature: float = 0.7, default_model: str = "gpt-4o-mini", **kwargs: Any):
    from langchain_openai import ChatOpenAI

    config = get_llm_config(default_model=default_model)
    return ChatOpenAI(
        model=config.model,
        api_key=config.api_key,
        base_url=config.base_url,
        temperature=temperature,
        **kwargs,
    )


DEFAULT_AUTOGEN_MODEL_INFO = {
    "vision": False,
    "function_calling": False,
    "json_output": False,
    "structured_output": False,
    "family": "unknown",
}


def create_autogen_openai_client(
    default_model: str = "Qwen3-14B-AWQ",
    model_info: dict[str, Any] | None = None,
    **kwargs: Any,
):
    from autogen_ext.models.openai import OpenAIChatCompletionClient

    config = get_llm_config(default_model=default_model)
    return OpenAIChatCompletionClient(
        model=config.model,
        api_key=config.api_key,
        base_url=config.base_url,
        model_info=model_info or DEFAULT_AUTOGEN_MODEL_INFO,
        **kwargs,
    )
