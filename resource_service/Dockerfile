FROM python:3.11.9

WORKDIR /app

COPY . .

RUN pip install fastapi

EXPOSE 8004

CMD ["uvicorn", "resource_service:resource_service", "--host", "0.0.0.0", "--port", "8004"]
