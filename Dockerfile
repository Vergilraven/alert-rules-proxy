FROM registry.cn-shenzhen.aliyuncs.com/vergil-private/python:3.12.7-alpine3.19

WORKDIR /opt
# 确保所有文件都被正确复制到容器中
COPY app app
COPY requirements.txt requirements.txt
# 安装依赖时确保包含 FastAPI 和 Uvicorn
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
# 添加调试命令以验证文件是否存在

# 修改 CMD 指令以反映新的文件路径
CMD ["uvicorn", "app.control_panel.main:app", "--host", "0.0.0.0", "--port", "8000"]