FROM python:3.11.9

WORKDIR /app

COPY . .

RUN pip install fastapi uvicorn requests

EXPOSE 8001

CMD ["uvicorn", "auth_service:auth_service", "--host", "0.0.0.0", "--port", "8001"]
