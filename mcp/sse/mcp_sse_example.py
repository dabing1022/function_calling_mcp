# -*- coding: utf-8 -*-
"""
MCP SSE 服务示例 - 使用官方FastMCP SSE支持
- 实现简单的算术运算工具（加减乘）
- 提供静态资源（Python之禅）
- 支持基本提示词模板
- 使用SSE（Server-Sent Events）作为传输方式
"""
import os
from datetime import datetime
from typing import Dict, Any, Optional, List

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

# 创建 MCP 服务器实例
mcp = FastMCP("SSE-Demo")
mcp.settings.mount_path = ""

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

@mcp.tool()
def now() -> str:
    """
    获取当前时间工具
    返回: 当前时间的字符串表示
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ========== 静态资源注册 ==========
@mcp.resource("file://zen_python.txt", name="zen_python", description="Zen of Python", mime_type="text/plain")
def get_zen_python() -> str:
    """
    返回: Zen of Python
    """
    # 获取当前脚本文件的绝对路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建 zen_python.txt 文件的绝对路径
    abs_file_path = os.path.join(script_dir, "zen_python.txt")
    
    # 读取并返回文件内容
    with open(abs_file_path, "r") as f:
        return f.read()

# ========== 提示词注册 ==========
@mcp.prompt()
def calculate_expression(expression: str) -> str:
    """
    计算数学表达式的提示词
    参数: expression - 数学表达式字符串
    返回: 提示词文本
    """
    return f"请计算以下数学表达式的结果: {expression}"

@mcp.prompt()
def debug_code(code: str, error: str) -> list[base.Message]:
    """
    代码调试的对话提示词
    参数: 
        code - 需要调试的代码
        error - 错误信息
    返回: 消息列表
    """
    return [
        base.UserMessage("我在运行以下代码时遇到了错误:"),
        base.UserMessage(f"```\n{code}\n```"),
        base.UserMessage(f"错误信息: {error}"),
        base.AssistantMessage("我来帮你分析这个错误。让我看看代码和错误信息...")
    ]

# ========== 为Web服务器添加静态文件支持 ==========
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

# 获取当前脚本文件的目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# 自定义首页路由处理函数
async def index(request):
    """返回首页HTML"""
    return FileResponse(os.path.join(script_dir, "index.html"))

# ========== 启动 MCP 服务器 ==========
if __name__ == "__main__":
    print("--------------------------------")
    print("MCP SSE 服务器启动中...")
    print("--------------------------------")
    
    try:
        mcp.settings.host = "127.0.0.1" # 或者 "localhost"
        mcp.settings.port = 8866 # 设置你想要的端口号，例如 8866
        # 这里改为使用默认的根路径而不是/sse子路径
        mcp.run(transport='sse')
        print(f"服务器已启动: http://{mcp.settings.host}:{mcp.settings.port}")
        print(f"API端点: http://{mcp.settings.host}:{mcp.settings.port}/messages/")
    except KeyboardInterrupt:
        print("\n服务器已停止") 