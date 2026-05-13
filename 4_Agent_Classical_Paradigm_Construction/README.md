# Chapter 4: Agent Classical Paradigm Construction

三种经典 Agent 构造范式的 Python 实现：ReAct、Plan-and-Solve、Reflection。

## Architecture

```
llm_client.py  +  tools.py          ← 公共基础设施
      ↓              ↓
  ReAct.py   Plan_and_solve.py   Reflection.py
```

`llm_client.py` 封装 LLM 调用，`tools.py` 提供计算器与搜索引擎工具。三个 Agent 范式共享这一基础设施。

## Files

| File | Description |
|------|-------------|
| `llm_client.py` | 封装 OpenAI 兼容 API 的客户端 `HelloAgentsLLM`，从 `.env` 读取配置 |
| `tools.py` | 工具执行器 + `calculate`（安全数学计算）+ `search`（SerpApi 搜索） |
| `ReAct.py` | ReAct Agent：Thought/Action 交替，调用工具获取外部信息 |
| `Plan_and_solve.py` | Plan-and-Solve：Planner 拆解步骤 → Executor 逐步执行 |
| `Reflection.py` | Reflection Agent：生成代码 → 反思审查 → 迭代优化 |

## Quick Start

```bash
cd 4_Agent_Classical_Paradigm_Construction

# 配置 .env（参考 .env.example）
cp .env.example .env  # 然后填入你的 API Key

# 运行任意 Agent
python ReAct.py
python Plan_and_solve.py
python Reflection.py
```

## Environment Variables

| Variable | Used By |
|----------|---------|
| `LLM_MODEL_ID` | `llm_client.py` |
| `LLM_API_KEY` | `llm_client.py` |
| `LLM_BASE_URL` | `llm_client.py` |
| `SERPAPI_API_KEY` | `tools.py` (search) |

`calculate` 是纯本地工具，无需额外 API Key。
