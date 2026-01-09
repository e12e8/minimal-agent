# Planner：把 Task 拆成可执行的 Steps
# 这里只做最简单的示例（工程中可以是 LLM）

def plan(task: str):
    return [
        f"分析任务：{task}",
        f"给出解决方案：{task}",
    ]
