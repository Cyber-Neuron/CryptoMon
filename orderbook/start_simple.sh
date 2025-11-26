#!/bin/bash

# 本地Order Book系统启动脚本（简化版）

echo "=== 本地Order Book维护系统 ==="
echo "正在启动系统..."

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python3"
    exit 1
fi

# 检查依赖
echo "检查依赖..."
if [ ! -f "requirements.txt" ]; then
    echo "错误: 未找到requirements.txt文件"
    exit 1
fi

# 安装依赖
echo "安装依赖包..."
pip3 install -r requirements.txt

# 启动系统
echo "启动Order Book系统..."
echo "API服务器将在 http://localhost:8000 启动"
echo "按 Ctrl+C 停止系统"
echo ""

# 直接运行Python程序
# 这样信号会直接传递给Python进程
python3 localorderbok.py 