FROM python:3.11.9

WORKDIR /app

COPY . .

RUN pip install fastapi uvicorn requests

EXPOSE 8002

CMD ["uvicorn", "session_service:session_service", "--host", "0.0.0.0", "--port", "8002"]
