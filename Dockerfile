FROM python:3.10.13-slim-bullseye

# 设置工作目录
WORKDIR /app

# 复制应用程序代码和依赖文件
COPY . /app

# 安装系统依赖
RUN apt-get update && apt-get install -y libpq-dev build-essential

# 安装 streamlit
RUN pip install --upgrade streamlit protobuf

# 将pip升级到最新版本
RUN pip install --upgrade pip

# 安装 Python 依赖
RUN pip install -r requirements.txt

# # 启动应用程序
# CMD ["streamlit", "run", "app.py"]

