#!/bin/bash

echo "🚀 资金流向监控仪表板 - 快速启动"
echo "=================================="

# 检查Node.js是否安装
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装，请先安装 Node.js"
    exit 1
fi

# 检查npm是否安装
if ! command -v npm &> /dev/null; then
    echo "❌ npm 未安装，请先安装 npm"
    exit 1
fi

echo "✅ Node.js 和 npm 已安装"

# 安装依赖
echo "📦 安装依赖..."
npm install

# 检查环境变量文件
if [ ! -f ".env.local" ]; then
    echo "⚠️  未找到 .env.local 文件"
    echo "请创建 .env.local 文件并设置 DATABASE_URL"
    echo "示例:"
    echo "DATABASE_URL=postgresql://username:password@host:port/database"
    echo ""
    echo "是否要创建示例 .env.local 文件？(y/n)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        echo "DATABASE_URL=postgresql://localhost:5432/walletmonitor" > .env.local
        echo "✅ 已创建示例 .env.local 文件"
        echo "⚠️  请根据你的实际数据库配置修改 DATABASE_URL"
    fi
else
    echo "✅ 找到 .env.local 文件"
fi

# 测试数据库连接
echo "🧪 测试数据库连接..."
if node test-local.js; then
    echo "✅ 数据库连接测试通过"
else
    echo "❌ 数据库连接测试失败"
    echo "请检查 DATABASE_URL 配置"
    exit 1
fi

# 启动开发服务器
echo "🌐 启动开发服务器..."
echo "应用将在 http://localhost:3000 启动"
echo "按 Ctrl+C 停止服务器"
echo ""

npm run dev 