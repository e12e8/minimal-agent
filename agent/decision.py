# decision.py
# Decision 层：根据步骤内容决定使用哪个工具（策略层）
# 本层不执行具体工具，只负责返回工具标识


def choose_tool(step: str) -> str:
    """
    根据当前步骤选择合适的工具。

    参数:
        step (str): 当前执行的步骤描述

    返回:
        str: 工具名称（例如 "tech" 或 "general"）
    """
    # 简单策略：如果步骤包含“分析”相关词汇，优先使用技术工具
    if "分析" in step:
        return "tech"
    # 默认使用通用工具
    return "general"
