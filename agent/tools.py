# Tool：被动执行，不进行决策或反思，仅返回执行结果。


def general_tool(step: str):
    """
    通用能力：以自然语言方式返回对步骤的完成说明（演示用）。

    参数:
    - step: 当前执行的步骤说明

    返回值:
    - dict: 包含 `content` 字段的结果描述
    """
    return {
        "content": f"[GeneralTool] 已完成：{step}"
    }


def tech_tool(step: str):
    """
    技术能力：模拟技术类工具的处理并返回结果（演示用）。

    参数:
    - step: 当前执行的步骤说明

    返回值:
    - dict: 包含 `content` 字段的结果描述
    """
    return {
        "content": f"[TechTool] 技术处理完成：{step}"
    }
