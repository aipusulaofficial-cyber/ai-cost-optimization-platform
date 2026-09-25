FROM python:3.12-slim
WORKDIR /app
COPY . .
CMD ["python","-c","from cost_platform import Budget; print('AI FinOps ready')"]
