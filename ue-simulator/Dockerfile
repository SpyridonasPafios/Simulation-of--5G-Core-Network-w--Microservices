FROM python:3.11.9

WORKDIR /app

COPY . .

RUN pip install requests

EXPOSE 8002

CMD ["python", "main.py"]