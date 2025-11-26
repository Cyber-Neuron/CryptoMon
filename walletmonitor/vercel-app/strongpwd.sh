#!/bin/bash

# 强密码生成脚本
# 格式: crypto:强密码
# 输出: 明文和base64编码

# 生成强密码的函数
generate_strong_password() {
    # 使用 openssl 生成随机字符，避免 tr 的字节序列问题
    local password=$(openssl rand -base64 24 | tr -d "=+/" | tr '[:upper:]' '[:lower:]' | head -c 20)
    
    # 确保密码包含至少一个大写字母、小写字母、数字和特殊字符
    local chars="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*"
    local upper=$(echo $chars | fold -w1 | grep -E '[A-Z]' | shuf -n1)
    local lower=$(echo $chars | fold -w1 | grep -E '[a-z]' | shuf -n1)
    local digit=$(echo $chars | fold -w1 | grep -E '[0-9]' | shuf -n1)
    local special=$(echo $chars | fold -w1 | grep -E '[!@#$%^&*]' | shuf -n1)
    
    # 构建最终密码
    local final_password="${upper}${lower}${digit}${special}"
    
    # 添加更多随机字符到32位
    local remaining_chars=$(echo $chars | fold -w1 | shuf -n 28 | tr -d '\n')
    final_password="${final_password}${remaining_chars}"
    
    echo "$final_password"
}

# 主程序
main() {
    echo "=== 强密码生成器 ==="
    echo
    
    # 生成强密码
    local strong_password=$(generate_strong_password)
    local formatted_password="crypto:$strong_password"
    
    # 输出明文
    echo "明文格式:"
    echo "$formatted_password"
    echo
    
    # 输出base64编码
    echo "Base64编码:"
    echo "$formatted_password" | base64
    echo
    
    # 验证base64解码
    echo "Base64解码验证:"
    echo "$formatted_password" | base64 | base64 -d
    echo
    
    echo "=== 生成完成 ==="
}

# 检查是否安装了必要的命令
if ! command -v openssl &> /dev/null; then
    echo "错误: 未找到 openssl 命令"
    echo "请安装 openssl 包"
    exit 1
fi

if ! command -v base64 &> /dev/null; then
    echo "错误: 未找到 base64 命令"
    echo "请安装 coreutils 包"
    exit 1
fi

# 运行主程序
main
