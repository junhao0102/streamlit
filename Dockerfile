FROM python:3.10.13-slim-bullseye

# 設置工作目錄
WORKDIR /app

# 複製當前目錄下的所有文件到工作目錄
COPY . /app


# 更新 pip
RUN pip install --upgrade pip

# 安裝依賴
RUN pip install -r requirements.txt


