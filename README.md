# Minimal Agent (Engineering-Oriented)

一个不依赖 LangChain 的最小 Agent 工程实现，用于演示：
- Planner / Decision / Tool / State / Reflection 的职责划分
- Agent 如何通过状态与反思形成闭环控制
- 工程视角下的 Agent 运行机制（非 Prompt Demo）
> 本项目刻意不引入 LangChain，
> 目的是让 Agent 的控制流显式可读，
> 便于理解与面试讲解。

## 为什么要做这个项目？

当前大量 Agent 示例停留在：
- Prompt 拼接
- 自动调用工具
- 隐式状态流转

这类实现难以回答工程问题，例如：
- 决策逻辑在哪里？
- 状态如何影响下一步行为？
- Retry 与普通循环的区别是什么？
- Agent 如何“知道什么时候该停？”

本项目以“工程可解释性”为目标，
用最小代码展示 Agent 的核心控制结构。


## Agent 架构概览

Task
 ↓
Planner        → 拆解为可执行 Steps
 ↓
Decision       → 为每个 Step 选择合适的 Tool
 ↓
Tool           → 被动执行，不参与决策
 ↓
Reflection     → 判断结果是否满足预期
 ↓
State          → 记录经验，影响后续决策


