FROM python:3.11.9

WORKDIR /app

RUN pip install requests

COPY . .

EXPOSE 8002

CMD ["python", "app/main.py"]