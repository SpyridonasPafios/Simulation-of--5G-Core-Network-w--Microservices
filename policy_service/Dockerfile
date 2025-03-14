FROM python:3.11.9

WORKDIR /app

COPY . .

RUN pip install fastapi

EXPOSE 8003

CMD ["uvicorn", "policy_service:policy_service", "--host", "0.0.0.0", "--port", "8003"]
