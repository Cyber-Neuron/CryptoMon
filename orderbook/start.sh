#!/bin/bash

# 本地Order Book系统启动脚本

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

# 设置信号处理
cleanup() {
    echo ""
    echo "正在关闭系统..."
    
    # 发送SIGTERM信号给Python进程
    if [ ! -z "$PYTHON_PID" ]; then
        echo "发送SIGTERM信号给进程 $PYTHON_PID..."
        kill -TERM $PYTHON_PID 2>/dev/null
        
        # 等待进程结束，最多等待10秒
        local count=0
        while kill -0 $PYTHON_PID 2>/dev/null && [ $count -lt 10 ]; do
            sleep 1
            count=$((count + 1))
            echo "等待进程退出... ($count/10)"
        done
        
        # 如果进程仍然存在，强制终止
        if kill -0 $PYTHON_PID 2>/dev/null; then
            echo "进程未响应SIGTERM，强制终止..."
            kill -KILL $PYTHON_PID 2>/dev/null
            sleep 1
        fi
    fi
    
    echo "系统已关闭"
    exit 0
}

# 注册信号处理
trap cleanup SIGINT SIGTERM

# 启动Python程序
echo "启动Python程序..."
python3 localorderbok.py &
PYTHON_PID=$!
echo "Python进程ID: $PYTHON_PID"

# 等待Python进程
wait $PYTHON_PID
EXIT_CODE=$?

echo "Python进程已退出，退出码: $EXIT_CODE"
exit $EXIT_CODE 