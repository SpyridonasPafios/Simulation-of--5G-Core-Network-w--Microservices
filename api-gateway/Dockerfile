# Use official Python image
FROM python:3.11.9

# Set working directory inside the container
WORKDIR /app

# Install dependencies
RUN pip install fastapi uvicorn requests prometheus-fastapi-instrumentator

# Copy the rest of the application code
COPY . .

# Expose the service port
EXPOSE 8000

# Run the microservice
CMD ["uvicorn", "app.main:gateway", "--host", "0.0.0.0", "--port", "8000"]
