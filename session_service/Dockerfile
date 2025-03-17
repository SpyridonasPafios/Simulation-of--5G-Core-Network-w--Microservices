FROM python:3.11.9

WORKDIR /app

RUN pip install fastapi

COPY . .

EXPOSE 8002

CMD ["uvicorn", "main:session_service", "--host", "0.0.0.0", "--port", "8002"]
