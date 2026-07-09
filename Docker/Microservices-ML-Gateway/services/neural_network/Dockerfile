FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY model.py .
EXPOSE 5004
CMD ["uvicorn", "model:app", "--host", "0.0.0.0", "--port", "5004"]