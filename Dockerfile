FROM python:3.10.13-slim-bullseye

# 设置工作目录
WORKDIR /app

# 复制应用程序代码和依赖文件
COPY . /app


# 将pip升级到最新版本
RUN pip install --upgrade pip

# 安装 Python 依赖
RUN pip install -r requirements.txt


