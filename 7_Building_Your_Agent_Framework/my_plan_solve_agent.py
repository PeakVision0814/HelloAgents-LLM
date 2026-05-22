import json
import re
from typing import Optional, Dict, List

from hello_agents import PlanAndSolveAgent, HelloAgentsLLM, Config, Message


DEFAULT_PROMPTS = {
    "planner": """
你是一个擅长拆解复杂问题的规划助手。请把下面的问题拆解为一个清晰、可执行的计划。

原始问题：{question}

请严格输出 JSON，不要输出任何额外说明，格式如下：
{{
  "problem": "原始问题",
  "steps": [
    {{"id": 1, "task": "步骤1描述"}},
    {{"id": 2, "task": "步骤2描述"}}
  ]
}}
""".strip(),
    "executor": """
你是一个严谨的执行助手。请根据给定的问题、完整计划和历史执行结果，只完成当前这一步。

原始问题：
{question}

完整计划：
{plan}

历史结果：
{history}

当前步骤：
{current_step}

请严格按下面格式输出，不要补充其他内容：
**执行结果:** <具体内容>
""".strip(),
    "summarizer": """
你是一个总结助手。请根据原始问题、执行计划和每一步的结果，整理出一个连贯、完整的最终答案。

原始问题：
{question}

执行计划：
{plan}

步骤结果：
{history}

请直接输出最终答案，不要附加解释。
""".strip(),
}


class MyPlanAndSolveAgent(PlanAndSolveAgent):
    """
    教学版 Plan-and-Solve Agent。

    特点：
    1. Planner 输出 JSON 计划
    2. Executor 输出标准化执行结果
    3. 所有步骤完成后再统一汇总最终答案
    """

    def __init__(
        self,
        name: str,
        llm: HelloAgentsLLM,
        system_prompt: Optional[str] = None,
        config: Optional[Config] = None,
        max_steps: int = 8,
        custom_prompts: Optional[Dict[str, str]] = None,
    ) -> None:
        super().__init__(
            name=name,
            llm=llm,
            system_prompt=system_prompt,
            config=config,
            custom_prompts=custom_prompts,
        )
        self.max_steps = max_steps
        self.prompts = self._merge_prompts(custom_prompts)
        print(f"✅ {name} 初始化完成，最大步骤数: {max_steps}")

    def run(self, input_text: str, **kwargs) -> str:
        print(f"\n🤖 {self.name} 开始处理问题: {input_text}")

        print("\n--- 正在生成计划 ---")
        plan = self._build_plan(input_text, **kwargs)
        if not plan:
            final_answer = "无法生成有效的行动计划，任务终止。"
            print(f"\n--- 任务终止 ---\n{final_answer}")
            self.add_message(Message(input_text, "user"))
            self.add_message(Message(final_answer, "assistant"))
            return final_answer

        if len(plan) > self.max_steps:
            final_answer = f"生成的计划共 {len(plan)} 步，超过最大步骤数 {self.max_steps}，任务终止。"
            print(f"\n--- 任务终止 ---\n{final_answer}")
            self.add_message(Message(input_text, "user"))
            self.add_message(Message(final_answer, "assistant"))
            return final_answer

        history_entries: List[str] = []

        print("\n--- 正在执行计划 ---")
        for i, step in enumerate(plan, 1):
            print(f"\n--- 第 {i} 步 ---")
            print(f"-> 正在执行步骤 {i}/{len(plan)}: {step}")

            execution_result = self._execute_step(
                question=input_text,
                plan=plan,
                history_entries=history_entries,
                current_step=step,
                **kwargs,
            )
            history_entries.append(f"步骤 {i}: {step}\n执行结果: {execution_result}")
            print(f"✅ 步骤 {i} 已完成，结果: {execution_result}")

        print("\n--- 正在汇总最终答案 ---")
        final_answer = self._summarize_answer(
            question=input_text,
            plan=plan,
            history_entries=history_entries,
            **kwargs,
        )

        print(f"\n--- 任务完成 ---\n最终答案: {final_answer}")
        self.add_message(Message(input_text, "user"))
        self.add_message(Message(final_answer, "assistant"))
        return final_answer

    def _merge_prompts(self, custom_prompts: Optional[Dict[str, str]]) -> Dict[str, str]:
        prompts = DEFAULT_PROMPTS.copy()
        if custom_prompts:
            prompts.update(custom_prompts)
        return prompts

    def _build_plan(self, question: str, **kwargs) -> List[str]:
        prompt = self.prompts["planner"].format(question=question)
        response_text = self._invoke(prompt, **kwargs)
        print(f"✅ 计划已生成:\n{response_text}")

        try:
            plan_data = json.loads(response_text)
        except json.JSONDecodeError as exc:
            print(f"❌ 解析计划时出错: {exc}")
            print(f"原始响应: {response_text}")
            return []

        steps = plan_data.get("steps", [])
        if not isinstance(steps, list):
            return []

        plan: List[str] = []
        for step in steps:
            if isinstance(step, dict):
                task = step.get("task")
                if isinstance(task, str) and task.strip():
                    plan.append(task.strip())
        return plan

    def _execute_step(
        self,
        question: str,
        plan: List[str],
        history_entries: List[str],
        current_step: str,
        **kwargs,
    ) -> str:
        history_text = "\n\n".join(history_entries) if history_entries else "无"
        prompt = self.prompts["executor"].format(
            question=question,
            plan=json.dumps(plan, ensure_ascii=False, indent=2),
            history=history_text,
            current_step=current_step,
        )
        response_text = self._invoke(prompt, **kwargs)
        return self._extract_execution_result(response_text)

    def _extract_execution_result(self, response_text: str) -> str:
        match = re.search(r"\*\*执行结果:\*\*\s*(.+)", response_text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return response_text.strip()

    def _summarize_answer(
        self,
        question: str,
        plan: List[str],
        history_entries: List[str],
        **kwargs,
    ) -> str:
        prompt = self.prompts["summarizer"].format(
            question=question,
            plan=json.dumps(plan, ensure_ascii=False, indent=2),
            history="\n\n".join(history_entries),
        )
        return self._invoke(prompt, **kwargs)

    def _invoke(self, prompt: str, **kwargs) -> str:
        messages = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": prompt})
        return self.llm.invoke(messages, **kwargs) or ""
