# Tool：被动执行，不思考，不决策

def general_tool(step: str):
    return {
        "content": f"[GeneralTool] 已完成：{step}"
    }


def tech_tool(step: str):
    return {
        "content": f"[TechTool] 技术处理完成：{step}"
    }
