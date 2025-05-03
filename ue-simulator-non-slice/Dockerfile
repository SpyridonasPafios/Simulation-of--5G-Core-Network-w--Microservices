FROM python:3.11.9

WORKDIR /app

RUN pip install fastapi uvicorn requests httpx==0.27.0


COPY . .

EXPOSE 8002

CMD ["python", "app/main.py"]