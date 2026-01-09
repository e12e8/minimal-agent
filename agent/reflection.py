# Reflection：判断结果是否满足预期
# 本模块负责“反思”工具返回的结果，决定是否接受或需要重试


def reflect(step: str, result: dict):
    """
    简单的反思判定函数：根据 result 内容判断是否接受。

    返回字典应包含键 `accept`（bool）和 `reason`（str），
    供调用方作为停止/重试的依据。
    """
    content = result["content"]

    # 极简示例：如果内容太短，认为不满意，要求重试
    if len(content) < 10:
        return {
            "accept": False,
            "reason": "结果过短"
        }

    # 否则认为可接受
    return {
        "accept": True,
        "reason": "结果可接受"
    }
