#!/bin/bash
password=$(openssl rand -base64 32 | tr -dc 'A-Za-z0-9!@#$%^&*()_+-=[]{}|;:,.<>?' | head -c 32)
formatted="crypto:$password"
echo "明文格式:"
echo "$formatted"
echo
echo "Base64编码:"
echo "$formatted" | base64
