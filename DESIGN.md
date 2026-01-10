# Minimal Agent 设计说明（工程版）

## 1. Agent 的职责边界
- Agent 是控制器，不是工具
- Agent 不直接生成答案，只组织能力

## 2. 为什么需要 Planner
- 将不可执行的 Task 转为可决策的 Steps
- Planner 不调用工具

## 3. Decision 的作用
- 基于 State 选择工具
- Decision 不执行、不反思

## 4. Tool 为什么是被动的
- Tool 不知道“下一步”
- Tool 只完成一次能力调用

## 5. State 的作用
- 记录 Step × Tool 的局部经验
- 记录 Tool 的全局经验
- 失败经验会降低未来选择概率

## 6. Reflection 的职责
- 判断结果是否满足预期
- 不直接控制流程，只提供建议

## 7. Agent 如何学习
- 成功 → 建立信任（streak）
- 失败 → 负反馈（failure）
- 决策随历史经验变化
