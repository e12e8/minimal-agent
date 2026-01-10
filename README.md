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



Minimal Agent 设计说明（工程版）
一、Agent 的定位与职责边界
Agent 是什么？

本项目中的 Agent 是一个控制器（Controller），其核心职责是：

在不确定环境下，组织能力、评估结果、积累经验，并逐步逼近目标。

Agent 明确“不做”的事情

为了工程可控性，本 Agent 刻意不做以下事情：

❌ 不在 Tool 内做决策

❌ 不在 Tool 内保存经验

❌ 不在 Decision 内修改状态

❌ 不让 Reflection 直接控制流程

❌ 不把 Planner 当成执行器

Agent 不是“会写 if/else 的脚本”，而是“组织协作的控制系统”。

二、整体运行结构（高层视图）
Task
 ↓
Planner（拆解目标）
 ↓
Step 1 ──┐
         │
      Decision（选能力）
         │
      Execution（用工具）
         │
      Reflection（评估结果）
         │
      State（沉淀经验）
         │
      ──→ 下一次 Decision


这是一条闭环因果链，不是线性流程。

三、为什么要有 Planner（而不是直接 Decision）
Planner 的职责

Planner 只做一件事：

把一个模糊目标，拆成“可评估的子目标（Step）”。

例如：

任务：解释 Agent 的运行机制
↓
Step 1：分析任务背景
Step 2：说明核心模块
Step 3：结合工程示例

Planner 刻意不做的事

❌ 不选择工具

❌ 不执行能力

❌ 不判断结果好坏

原因：

如果 Planner 参与执行，它就会变成一个“弱 Agent”，系统会迅速失控。

四、Decision 为什么必须独立存在
Decision 层的本质

Decision 的本质是：

在多个“可用能力”中，基于经验选择“当前最可能成功的那个”。

Decision 层的约束（非常重要）

Decision 层遵守三条铁律：

只读 State

不执行任何 Tool

只输出“选择结果”

为什么不能在 Tool 内做 Decision？

如果 Tool 自己决定下一步：

Agent 会失去全局视角

不同 Tool 会互相“抢控制权”

无法做统一反思与经验累积

Tool 一旦会“决定”，Agent 就不再是 Agent。

五、为什么 Tool 必须是“被动的”
Tool 的设计原则

在本项目中，Tool 是：

纯函数化能力单元

特点：

输入：Step 描述

输出：结果事实（content / tool / metadata）

不读 State

不写 State

不知道自己“用得好不好”

工程意义

这样做带来的好处是：

Tool 可复用

Tool 可替换

Tool 可测试

Tool 可被不同 Agent 使用

Tool ≠ Agent，Tool ≠ 决策者，Tool = 能力插件

六、Reflection 在“反思什么”
Reflection 不等于 Retry

Reflection 的职责不是：

“要不要再来一次？”

而是：

“这次结果，值不值得信任？”

Reflection 评估的维度包括：

输出是否完整

输出是否明显不匹配当前 Step

该 Tool 在历史上是否经常失败

是否出现连续失败（streak）

Reflection 的输出

Reflection 只输出结构化判断：

ReflectionDecision(
    is_success: bool,
    confidence: float,
    should_retry: bool,
    reason: str
)


Reflection 不控制流程，只提供判断依据。

七、State 的真正作用（不是缓存）
State 不是缓存

缓存回答的是：

“这个结果算过了吗？”

State 回答的是：

“在类似情况下，什么更值得信任？”

State 中保存的不是结果，而是“经验”

State 维护的信息包括：

每个 Tool 的成功次数

每个 Tool 的失败次数

每个 Tool 的连续成功 / 连续失败

跨 Step 继承的经验统计

为什么跨 Step 继承很重要？

因为在真实任务中：

工具的可靠性，往往与具体 Step 无关，而与工具本身有关。

八、Retry 和 for 循环的本质区别
for 循环是什么？
for i in range(3):
    run()


这是：

次数驱动

Retry 是什么？

Retry 是：

基于“结果质量”的条件性再次尝试

特点：

可能一次都不 retry

可能只在特定 Tool 上 retry

可能改变策略后 retry

Retry 是“反思驱动的控制逻辑”，不是重复执行。

九、这个 Agent 能解决什么问题？

这个 Agent 适合解决：

需要多能力协作的问题

工具质量不稳定的问题

需要逐步逼近正确结果的问题

需要“可解释决策过程”的业务场景

例如：

技术方案生成

需求拆解

测试用例生成

知识补全型任务

十、这个 Agent 刻意没做什么（面试加分项）

本项目 刻意没有：

自动无限 Retry

LLM 内部思维暴露

复杂状态机

强化学习

LangChain / LangGraph 依赖

原因很简单：

工程可控性 > 智能炫技