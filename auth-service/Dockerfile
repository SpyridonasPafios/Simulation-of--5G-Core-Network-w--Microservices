FROM python:3.11.9

WORKDIR /app

RUN pip install fastapi

COPY . .

EXPOSE 8001

CMD ["uvicorn", "app.main:auth_service", "--host", "0.0.0.0", "--port", "8001"]
