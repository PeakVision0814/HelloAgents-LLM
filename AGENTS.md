# AGENTS.md

本文件为在本仓库内工作的 AI/Codex/Claude 类代理提供协作说明。

## 项目定位

- 这是一个基于 [Datawhale Hello-Agents](https://github.com/datawhalechina/hello-agents) 的个人学习练习仓库。
- 代码、提示词和文档以中文为主，整体偏教学演示，不是生产级项目。
- 修改时优先保持“便于阅读、便于教学、便于单文件运行”的风格，不要无必要地工程化重构。

## 仓库结构

- `1_Introduction_to_Agents/`
  - `travel_agent.py`：旅行助手 Agent，演示 Thought -> Action -> Observation 循环。
  - 依赖联网、LLM API 与 Tavily。
- `2_History_of_Agents/`
  - `ELIZA.py`：规则式对话系统，零外部依赖。
- `3_Fundamentals_of_LLMs/`
  - `N_gram.py`、`BPE.py`、`Word_Embedding.py`、`Transformer.py`、`Call LLM.py`。
  - `Call LLM.py` 文件名带空格，执行命令时必须加引号。
- `4_Agent_Classical_Paradigm_Construction/`
  - `llm_client.py`：共享 OpenAI 兼容客户端。
  - `tools.py`：`calculate` 与 `search` 工具。
  - `ReAct.py`、`Plan_and_solve.py`、`Reflection.py`：三种经典 Agent 范式示例。
- `5_Building_Agents_with_Low_Code_Platforms/`
  - Dify 的 `.yml` / `.zip` 与 n8n 的 `.json` 工作流导出文件。
  - 基本不涉及 Python 代码修改。
- `6_Framework_Development_Practice/`
  - `Langgraph/Dialogue_System.py`：LangGraph + Tavily 的三步问答工作流。
  - `AutoGenDemo/AutoGenDemo.py`：AutoGen 多代理协作示例。
  - `AutoGenDemo/requirements.txt`：该示例的补充依赖列表。

## 环境与依赖

- 推荐 Python `3.10+`。
- 根目录可使用：

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

- 第 6 章中的 LangGraph 示例额外依赖 `langgraph`、`langchain-openai`、`langchain-core`，当前根 `requirements.txt` 未完整覆盖这部分。
- 需要联网或 API Key 的示例主要在第 1、4、6 章。
- 根目录存在 `.env.example`，优先参考它配置本地 `.env`，不要提交真实密钥。

## 已知注意点

- `1_Introduction_to_Agents/travel_agent.py` 当前把演示用模型参数和 Tavily Key 直接写在源码里；如果改动该文件，优先改成读取本地环境变量，不要新增或保留真实密钥。
- `4_Agent_Classical_Paradigm_Construction/` 里的脚本依赖同目录下的 `llm_client.py` 与 `tools.py`，修改时注意不要破坏这些共享接口。
- `6_Framework_Development_Practice/AutoGenDemo/AutoGenDemo.py` 当前工作区中可能已有用户未提交改动；修改前先读清楚，不要覆盖用户调整。
- 根 `README.md` 是仓库总入口；如果新增章节、调整依赖或改变运行方式，应同步更新根 README。
- 各章节以“直接运行单脚本”作为主要使用方式，除非有明确收益，不要强行改造成包结构。

## 文档与代码修改约定

- 优先保持中文注释、中文说明与中文输出风格一致。
- 修改示例代码时，尽量保留教学型打印输出，避免把流程信息全部删掉。
- 如果行为或依赖发生变化，至少同步更新以下文档之一：
  - 根 `README.md`
  - 对应章节下的 `README.md`
- 新增文件名时尽量避免空格；若必须引用已有带空格或中文路径的文件，命令中请显式加引号。

## 验证建议

- 本仓库没有统一测试入口，也没有成体系的自动化测试。
- 验证方式以“运行被改动的单个脚本”或“检查文档命令是否与真实目录一致”为主。
- 涉及外部 API、联网搜索、模型下载的脚本，如果本地没有密钥或网络权限，应在最终说明里明确写出未实际运行。

## 安全规则：禁止批量删除

在本仓库内必须遵守以下删除限制：

1. 禁止批量删除文件或目录。
2. 任何删除操作都必须逐个执行，一次只能删除一个明确指定的文件或一个明确指定的目录。
3. 不允许使用会一次删除多个目标的命令、通配符、递归批量删除、管道批量删除，或基于搜索结果批量删除。
4. 在执行删除前，必须先说明将要删除的单个目标路径，并确认该目标是唯一目标。
5. 如果任务需求涉及批量删除文件或目录，必须立即停止，不得继续执行删除命令。

用户要求批量删除时，请使用这段回复：

“根据这个项目的安全规则，我不能代为批量删除文件或目录。为避免误删，我必须停止当前删除操作。请你手动完成这次批量删除，或者把要删除的目标逐个发给我，我可以按单个目标逐项帮你处理。”
