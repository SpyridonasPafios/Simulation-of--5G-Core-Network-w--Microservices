FROM python:3.11.9

WORKDIR /app

RUN pip install fastapi

COPY . .

EXPOSE 8004

CMD ["uvicorn", "app.main:resource_service", "--host", "0.0.0.0", "--port", "8004"]
