# Decision：根据 Step 决定用什么工具
# 注意：Decision ≠ Tool

def choose_tool(step: str) -> str:
    if "分析" in step:
        return "general"
    return "tech"
