# tools.py
# Tool 是被动能力：不做决策，只负责执行特定动作并返回结果

def general_tool(step: str) -> dict:
    """
    通用工具：对输入步骤做一般性说明或知识返回。

    参数:
        step (str): 当前要执行的步骤描述

    返回:
        dict: 包含 `status`、`content`、`confidence`、`tool` 的结果字典
    """
    # 返回一个模拟的工具执行结果，包含置信度和文本内容
    return {
        "status": "ok",
        "content": f"【通用知识】{step}",
        "confidence": 0.6,
        "tool": "general"
    }


def tech_tool(step: str) -> dict:
    """
    技术工具：针对包含“分析”或技术相关步骤时提供更详细、更高置信度的解释。

    参数与返回值同 `general_tool`。
    """
    # 返回一个模拟的技术性说明，置信度较高
    return {
        "status": "ok",
        "content": f"【技术解释】{step}",
        "confidence": 0.9,
        "tool": "tech"
    }
