# -*- coding: utf-8 -*-
"""
MCP Streamable 服务示例 - 使用官方MCP SDK的streamable-http支持
- 实现简单的算术运算工具（加减乘）
- 提供静态资源（Python之禅）
- 支持基本提示词模板
- 使用FastAPI挂载streamable-http应用
"""
import os
import sys
import logging
import contextlib
from datetime import datetime

import uvicorn
from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base
from fastapi.routing import APIRoute, Mount

# 设置日志
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("mcp-streamable")

# 创建 MCP 服务器实例
mcp = FastMCP("mcp-streamable-example", stateless_http=True, json_response=True)

# ========== 注册工具 ==========
@mcp.tool()
def add(a: int, b: int) -> int:
    """
    两数相加工具
    参数: a, b - 两个整数
    返回: 相加结果
    """
    logger.info(f"调用add工具: {a} + {b}")
    return a + b

@mcp.tool()
def sub(a: int, b: int) -> int:
    """
    两数相减工具
    参数: a, b - 两个整数
    返回: 相减结果
    """
    logger.info(f"调用sub工具: {a} - {b}")
    return a - b

@mcp.tool()
def mul(a: int, b: int) -> int:
    """
    两数相乘工具
    参数: a, b - 两个整数
    返回: 相乘结果
    """
    logger.info(f"调用mul工具: {a} * {b}")
    return a * b

@mcp.tool()
def now() -> str:
    """
    获取当前时间工具
    返回: 当前时间的字符串表示
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"调用now工具: {current_time}")
    return current_time

# ========== 注册静态资源 ==========
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
        content = f.read()
        logger.info("获取zen_python资源")
        return content

# ========== 注册提示词 ==========
@mcp.prompt()
def calculate_expression(expression: str) -> str:
    """
    计算数学表达式的提示词
    参数: expression - 数学表达式字符串
    返回: 提示词文本
    """
    logger.info(f"使用calculate_expression提示词: {expression}")
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
    logger.info(f"使用debug_code提示词")
    return [
        base.UserMessage("我在运行以下代码时遇到了错误:"),
        base.UserMessage(f"```\n{code}\n```"),
        base.UserMessage(f"错误信息: {error}"),
        base.AssistantMessage("我来帮你分析这个错误。让我看看代码和错误信息...")
    ]

# 创建lifespan上下文管理器
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI应用的生命周期管理"""
    async with mcp.session_manager.run():
        yield

# 创建FastAPI应用
app = FastAPI(lifespan=lifespan)

# 将MCP服务挂载到根路径，避免重复/mcp嵌套
app.mount("/", mcp.streamable_http_app())

# 添加根路径响应
@app.get("/")
async def root():
    """根路径处理函数"""
    return {
        "name": "MCP Streamable HTTP服务器",
        "version": "1.0.0",
        "endpoints": {
            "mcp": "/mcp"
        }
    }

def print_routes(routes, prefix="", level=0):
    indent = "  " * level
    for route in routes:
        if hasattr(route, "methods"):
            print(f"{indent}- {prefix}{route.path} [{route.methods}]")
        elif isinstance(route, Mount):
            print(f"{indent}- {prefix}{route.path} [Mount]")
            # 递归打印子应用的路由，带缩进
            if hasattr(route.app, 'routes'):
                print_routes(route.app.routes, prefix=prefix+route.path, level=level+1)
        else:
            print(f"{indent}- {prefix}{route.path} [Unknown Type]")

# 主函数
def main():
    """主函数"""
    print("--------------------------------")
    print("MCP Streamable 服务器启动中...")
    print("--------------------------------")
    
    host = "127.0.0.1"
    port = 8867
    
    print("服务器配置:")
    print(f"- 名称: {mcp.name}")
    print(f"- 地址: {host}:{port}")
    print(f"- 挂载路径: /mcp")
    # print(f"- API路径: /mcp/") # 暂时注释掉，因为挂载点已经说明了路径
    print(f"- 传输方式: streamable-http (FastAPI)")
    
    # ========== 打印FastAPI和MCP子应用路由，方便调试 ==========
    print("\nFastAPI 主应用路由:")
    print_routes(app.routes)
    print("==================================================\n")
    
    try:
        # 使用uvicorn启动FastAPI应用
        uvicorn.run(app, host=host, port=port)
    except KeyboardInterrupt:
        print("\n服务器已停止")
        sys.exit(0)
    except Exception as e:
        print(f"\n启动服务器时出错: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 