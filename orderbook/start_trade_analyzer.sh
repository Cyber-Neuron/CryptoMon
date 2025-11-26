#!/bin/bash

# 期货交易数据分析程序启动脚本

echo "=== 期货交易数据分析程序 ==="
echo "正在启动程序..."

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

# 检查本地Order Book系统是否运行
echo "检查本地Order Book系统..."
if ! curl -s http://localhost:8000/status > /dev/null; then
    echo "警告: 本地Order Book系统未运行"
    echo "请先启动 localorderbok.py:"
    echo "  python3 localorderbok.py"
    echo "或者使用启动脚本:"
    echo "  ./start_simple.sh"
    echo ""
    read -p "是否继续启动交易分析程序? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "程序启动已取消"
        exit 1
    fi
fi

# 启动交易分析程序
echo "启动期货交易数据分析程序..."
echo "按 Ctrl+C 停止程序"
echo ""

# 直接运行Python程序
python3 future_trade_analyzer.py 