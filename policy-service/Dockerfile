FROM python:3.11.9

WORKDIR /app

RUN pip install fastapi

COPY . .

EXPOSE 8003

CMD ["uvicorn", "app.main:policy_service", "--host", "0.0.0.0", "--port", "8003"]
