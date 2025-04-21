#!/bin/bash

# 更新系统
echo "Updating system..."
sudo apt update

# 安装必要的工具
echo "Installing wget..."
sudo apt install -y wget

# 下载 Google Chrome 安装包
echo "Downloading Google Chrome..."
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

# 安装 Google Chrome
echo "Installing Google Chrome..."
sudo apt install -y ./google-chrome-stable_current_amd64.deb

# 验证安装是否成功
echo "Checking Google Chrome version..."
google-chrome --version
