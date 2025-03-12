# Use official Python image
FROM python:3.11.9

# Set working directory inside the container
WORKDIR /app

# Copy the microservice code
COPY . .

# Install dependencies
RUN pip install fastapi uvicorn requests

# Expose the service port
EXPOSE 8001

# Run the microservice
CMD ["uvicorn", "auth_service:auth_service", "--host", "0.0.0.0", "--port", "8001"]
