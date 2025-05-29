# -*- coding: utf-8 -*-
"""
MCP FastMCP 极简经典例子
- 展示如何注册一个工具（add）和一个资源（greeting）
- 适合团队讲解 MCP 的基本用法
"""
import os
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

# 创建 MCP 服务器实例，名字随意
mcp = FastMCP("Demo")

# ========== 工具注册 ==========
@mcp.tool()
def add(a: int, b: int) -> int:
    """
    两数相加工具
    参数: a, b - 两个整数
    返回: 相加结果
    """
    return a + b

@mcp.tool()
def sub(a: int, b: int) -> int:
    """
    两数相减工具
    参数: a, b - 两个整数
    返回: 相减结果
    """
    return a - b


@mcp.tool()
def mul(a: int, b: int) -> int:
    """
    两数相乘工具
    参数: a, b - 两个整数
    返回: 相乘结果
    """
    return a * b

# ========== 资源注册 ==========
# 目前 Claude App以及其他套壳 App 还不支持动态资源，所以暂时不能使用
@mcp.resource("greeting://{name}", name="greeting", description="动态问候资源", mime_type="text/plain")
def get_greeting(name: str) -> str:
    """
    动态问候资源
    参数: name - 用户名
    返回: 个性化问候语
    """
    return f"Hello, {name}, this is a greeting resource!"

# Claude App 支持静态资源，所以可以正常使用
@mcp.resource("file://zen_python.txt", name="zen_python", description="Zen of Python", mime_type="text/plain")
def get_zen_python() -> str:
    """
    返回: Zen of Python
    """
    # 获取当前脚本文件的绝对路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建 zen_python.txt 文件的绝对路径，确保它在脚本文件所在的目录
    abs_file_path = os.path.join(script_dir, "zen_python.txt")
    with open(abs_file_path, "r") as f:
        return f.read()


@mcp.prompt()
def review_code(code: str) -> str:
    return f"Please review this code:\n\n{code}"


@mcp.prompt()
def debug_error(error: str) -> list[base.Message]:
    return [
        base.UserMessage("I'm seeing this error:"),
        base.UserMessage(error),
        base.AssistantMessage("I'll help debug that. What have you tried so far?"),
    ]


# ========== 启动 MCP 服务器 ==========
if __name__ == "__main__":
    # 用 stdio 作为传输方式，适合本地演示和桌面端集成
    print("--------------------------------")
    print("MCP 服务器启动")
    print("--------------------------------")
    mcp.run(transport='stdio')
