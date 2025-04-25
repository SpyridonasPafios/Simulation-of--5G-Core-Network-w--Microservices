FROM python:3.11.9

WORKDIR /app

RUN pip install fastapi uvicorn requests prometheus-fastapi-instrumentator

COPY . .

EXPOSE 8002

CMD ["uvicorn", "app.main:session_service", "--host", "0.0.0.0", "--port", "8002"]
