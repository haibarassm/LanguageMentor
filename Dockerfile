FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 赋予测试脚本执行权限
RUN chmod +x run_tests.sh

# 运行测试用例
RUN ./run_tests.sh

# 暴露端口
EXPOSE 7860

# 启动应用
CMD ["python", "src/main.py"]
