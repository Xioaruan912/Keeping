#/bin/sh
echo "开始初始化环境"
sudo apt update -y
sudo apt install libgl1-mesa-glx -y
apt install python3-pip -y
apt install unzip -y
sudo apt-get install libatk1.0-0 -y
apt --fix-broken install -y 
echo "配置基础环境结束"