# AutoGenDemo：多角色协作示例

本目录演示一个基于 AutoGen 的“软件开发团队协作”流程，包含四个角色：
- `ProductManager`：需求分析与拆解
- `Engineer`：实现方案与代码产出
- `CodeReviewer`：代码审查
- `UserProxy`：验收与终止对话

入口脚本是 [AutoGenDemo.py](./AutoGenDemo.py)。

## 目录结构

```text
AutoGenDemo/
├─ AutoGenDemo.py
├─ requirements.txt
└─ roles/
   ├─ registry.py
   ├─ product_manager.py
   ├─ engineer.py
   ├─ code_reviewer.py
   ├─ user_proxy.py
   └─ __init__.py
```

## 环境准备

建议使用 `agent_study` conda 环境。

```bash
conda activate agent_study
pip install -r 6_Framework_Development_Practice/AutoGenDemo/requirements.txt
```

并确保仓库根目录 `.env` 已配置（参考 `.env.example`）：

```env
LLM_MODEL_ID=your-model-id
LLM_API_KEY=your-api-key
LLM_BASE_URL=https://your-api-endpoint
LLM_TIMEOUT=60
```

本示例通过根目录 `llm_clients.py` 读取 `.env` 并创建 AutoGen 模型客户端。

## 运行方式

在仓库根目录执行：

```bash
conda activate agent_study
python 6_Framework_Development_Practice/AutoGenDemo/AutoGenDemo.py
```

预期流程：
1. 初始化模型客户端
2. 根据角色注册表创建参与者
3. 运行 `RoundRobinGroupChat`
4. `UserProxy` 输出 `TERMINATE` 后结束

## 如何增减角色

角色装配集中在 [roles/registry.py](./roles/registry.py)。

### 新增角色

1. 在 `roles/` 下新增角色文件，例如 `security_reviewer.py`
2. 实现工厂函数，例如 `create_security_reviewer(model_client)`
3. 在 `ROLE_BUILDERS` 中注册角色键
4. 在 `DEFAULT_ROLE_SEQUENCE` 中加入该角色键

### 删除或调整角色顺序

只需要修改 `DEFAULT_ROLE_SEQUENCE`，主流程无需改动。

## 关键实现点

- 团队编排：`RoundRobinGroupChat`
- 终止条件：`TextMentionTermination("TERMINATE")`
- 参与者组装：`build_participants()`（位于 `roles/registry.py`）
- 模型客户端：`create_autogen_openai_client()`（来自根目录 `llm_clients.py`）

## 常见问题

### `ModuleNotFoundError: No module named 'autogen_agentchat'`

通常是 Python 环境不正确。请确认：
- 已执行 `conda activate agent_study`
- 已安装本目录 `requirements.txt`

### 启动时报配置错误

请检查根目录 `.env` 是否存在，且以下键名正确：
- `LLM_MODEL_ID`
- `LLM_API_KEY`
- `LLM_BASE_URL`

### 对话无法结束

请确认 `UserProxy` 仍使用脚本模式输入函数，并返回包含 `TERMINATE` 的文本。
