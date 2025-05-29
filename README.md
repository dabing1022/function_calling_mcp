# Function Calling & MCP函数调用示例项目

这个项目展示了使用Model Control Protocol (MCP) 实现大模型函数调用的不同方法。

## 项目结构

```
function_calling_mcp/
├── mcp/                      # MCP服务实现示例
│   ├── streamable/           # 基于FastAPI的streamable-http实现
│   ├── sse/                  # 基于SSE的实现
│   └── stdio/                # 基于标准输入输出的实现
├── function_calling/         # 函数调用示例
└── no_function_calling/      # 不使用函数调用的示例
```

## 主要功能

- 提供多种传输方式的MCP服务实现
- 演示基本的函数调用（加减乘、时间获取等）
- 支持静态资源访问（Python之禅文本）
- 支持提示词模板

## 说明

每个子目录都包含独立的示例，可以根据不同的集成需求选择合适的实现方式：

- **streamable** - 适合Web服务集成，基于FastAPI实现
- **sse** - 适合需要实时推送的场景
- **stdio** - 适合命令行工具和本地应用集成

## 开发环境

- Python 3.9+
- 依赖列表在各子目录的requirements.txt中 