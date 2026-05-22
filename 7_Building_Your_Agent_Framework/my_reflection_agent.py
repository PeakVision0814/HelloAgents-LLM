from typing import Optional, Dict, List

from hello_agents import ReflectionAgent, HelloAgentsLLM, Config, Message


DEFAULT_PROMPTS = {
    "initial": """
你是一个认真、可靠的 AI 助手。请先根据任务直接给出一个尽可能完整的初稿。

任务：{task}

请直接输出结果，不要额外解释你的思考过程。
""".strip(),
    "reflect": """
你现在是一位严格的审稿人，请检查下面这份结果是否存在问题，并提出具体改进意见。

原始任务：{task}

当前结果：
{content}

如果结果已经足够好，请只回复“无需改进”。
如果仍可优化，请明确指出不足，并给出可执行的修改建议。
""".strip(),
    "refine": """
请根据反馈意见改进你的结果。

原始任务：{task}

上一版结果：
{last_attempt}

反馈意见：
{feedback}

请直接输出改进后的最终内容，不要附加解释。
""".strip(),
}


class ReflectionMemory:
    """保存执行结果与反思反馈，便于教学演示。"""

    def __init__(self) -> None:
        self.records: List[Dict[str, str]] = []

    def add_record(self, record_type: str, content: str) -> None:
        self.records.append({"type": record_type, "content": content})
        print(f"📝 已记录一条 {record_type} 信息")

    def get_last_execution(self) -> str:
        for record in reversed(self.records):
            if record["type"] == "execution":
                return record["content"]
        return ""

    def get_trajectory(self) -> str:
        chunks: List[str] = []
        for record in self.records:
            if record["type"] == "execution":
                chunks.append(f"--- 执行结果 ---\n{record['content']}")
            elif record["type"] == "reflection":
                chunks.append(f"--- 反思反馈 ---\n{record['content']}")
        return "\n\n".join(chunks)


class MyReflectionAgent(ReflectionAgent):
    """
    教学版 Reflection Agent。

    参考第 4 章 Reflection 示例，实现：
    1. 初始生成
    2. 自我反思
    3. 根据反馈迭代优化
    """

    def __init__(
        self,
        name: str,
        llm: HelloAgentsLLM,
        system_prompt: Optional[str] = None,
        config: Optional[Config] = None,
        max_iterations: int = 3,
        custom_prompts: Optional[Dict[str, str]] = None,
    ) -> None:
        super().__init__(
            name=name,
            llm=llm,
            system_prompt=system_prompt,
            config=config,
            max_iterations=max_iterations,
            custom_prompts=custom_prompts,
        )
        self.prompts = self._merge_prompts(custom_prompts)
        self.memory = ReflectionMemory()
        print(f"✅ {name} 初始化完成，最大反思轮数: {max_iterations}")

    def run(self, input_text: str, **kwargs) -> str:
        print(f"\n🤖 {self.name} 开始处理任务: {input_text}")
        self.memory = ReflectionMemory()

        print("\n--- 正在进行初始尝试 ---")
        initial_prompt = self.prompts["initial"].format(task=input_text)
        current_result = self._get_llm_response(initial_prompt, **kwargs)
        self.memory.add_record("execution", current_result)

        for i in range(self.max_iterations):
            print(f"\n--- 第 {i + 1}/{self.max_iterations} 轮迭代 ---")

            print("\n-> 正在进行反思...")
            reflect_prompt = self.prompts["reflect"].format(
                task=input_text,
                content=current_result,
            )
            feedback = self._get_llm_response(reflect_prompt, **kwargs)
            self.memory.add_record("reflection", feedback)

            if self._should_stop(feedback):
                print("\n✅ 反思认为结果已无需改进，任务完成。")
                break

            print("\n-> 正在进行优化...")
            refine_prompt = self.prompts["refine"].format(
                task=input_text,
                last_attempt=current_result,
                feedback=feedback,
            )
            current_result = self._get_llm_response(refine_prompt, **kwargs)
            self.memory.add_record("execution", current_result)

        final_result = self.memory.get_last_execution()
        print(f"\n--- 任务完成 ---\n最终结果:\n{final_result}")

        self.add_message(Message(input_text, "user"))
        self.add_message(Message(final_result, "assistant"))
        return final_result

    def get_reflection_trajectory(self) -> str:
        """返回本轮任务的执行与反思轨迹。"""
        return self.memory.get_trajectory()

    def _merge_prompts(self, custom_prompts: Optional[Dict[str, str]]) -> Dict[str, str]:
        prompts = DEFAULT_PROMPTS.copy()
        if custom_prompts:
            prompts.update(custom_prompts)
        return prompts

    def _get_llm_response(self, prompt: str, **kwargs) -> str:
        messages = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": prompt})
        return self.llm.invoke(messages, **kwargs) or ""

    def _should_stop(self, feedback: str) -> bool:
        normalized_feedback = feedback.strip().lower()
        stop_signals = [
            "无需改进",
            "不需要改进",
            "已经很好",
            "已达到最佳",
            "no need for improvement",
            "no further improvement",
        ]
        return any(signal in normalized_feedback for signal in stop_signals)
