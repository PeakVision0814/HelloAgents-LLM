# Chapter 5: Building Agents with Low-Code Platforms

使用 Dify 和 n8n 等低代码平台搭建 Agent 工作流，无需手写循环逻辑。

## Files

| File | Platform | Description |
|------|----------|-------------|
| `Chatflow-AI_news-draft-9211.zip` | Dify | AI 新闻稿生成 Chatflow，可直接导入 Dify |
| `超级智能个人助手.yml` | Dify | 多功能个人助手 DSL 工作流 |
| `HelloAgent_n8nCase.json` | n8n | Gmail 触发 + AI 处理的自动化工作流 |

## How to Use

### Dify

1. 登录 Dify，进入 **Studio** → **Import**
2. 上传 `.yml` 或 `.zip` 文件
3. 在对应节点填入 API Key，发布即可使用

### n8n

1. 登录 n8n，点击 **Import from File**
2. 上传 `.json` 文件
3. 配置 Gmail 触发器和 LLM 节点的凭据

## Key Concepts

- **Chatflow vs Workflow**: Dify 的对话式编排 vs 流程式编排
- **n8n Automation**: 事件触发（如 Gmail 收信）→ AI 处理 → 结果输出
- 低代码平台让 Agent 开发重心从"写代码"转向"设计交互流程"
