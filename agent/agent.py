# Agent = 控制中枢
# 负责组织 Planner / Decision / Tool / Reflection / State
# 注意：Agent 的控制权（执行流程和重试逻辑）始终位于本文件中的 `run_agent` 函数内

from agent.planner import plan
from agent.decision import choose_tool
from agent.tools import general_tool, tech_tool
from agent.state import State
from agent.reflection import reflect

TOOL_MAP = {
    "general": general_tool,
    "tech": tech_tool,
}


def run_agent(task: str) -> str:
    print(f"\n[Agent] 接收到任务：{task}")

    state = State()
    steps = plan(task)

    final_output = ""

    for step in steps:
        print(f"\n[Step] {step}")

        # 重试控制：记录重试次数，并设置最大重试上限
        retry_count = 0
        max_retry = 2

        # Task → Tool → Result → Reflection → Retry 的循环控制
        # 使用 while True 循环以便在 reflection 决定不接受时重试
        while True:
            # ---------- Decision ----------
            tool_name = choose_tool(step)
            tool_func = TOOL_MAP[tool_name]
            print(f"→ Decision：选择工具 [{tool_name}]")

            # ---------- Execution ----------
            result = tool_func(step)
            print(f"→ Tool 返回：{result['content']}")

            # ---------- Reflection ----------
            # reflection 用于判断当前工具返回的结果是否可接受（控制停止条件）
            reflection = reflect(step, result)
            print(f"→ Reflection：{reflection}")

            # ---------- State ----------
            state.save(step, result, reflection)

            # 如果 reflection 表示接受，则结束当前步骤的重试循环
            if reflection["accept"]:
                final_output += result["content"] + "\n"
                break

            # 增加重试计数；若超过上限则强制接受当前结果并退出循环
            retry_count += 1
            if retry_count > max_retry:
                print("→ 超过最大重试次数，强制接受结果")
                final_output += result["content"] + "\n"
                break

    return final_output
