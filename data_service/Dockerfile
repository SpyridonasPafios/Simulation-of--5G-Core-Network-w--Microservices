FROM python:3.11.9

WORKDIR /app

COPY . .

RUN pip install fastapi

EXPOSE 8005

CMD ["uvicorn", "data_service:data_service", "--host", "0.0.0.0", "--port", "8005"]
