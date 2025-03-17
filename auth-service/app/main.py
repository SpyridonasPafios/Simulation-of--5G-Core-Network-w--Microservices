from fastapi import FastAPI
import os

auth_service = FastAPI()

@auth_service.post("/authenticate")
async def authenticate(request: dict):
    stress_cpu(3, request.get("load_factor", 1))
    stress_ram(2, request.get("load_factor", 1))
    return {"status": "authenticated"}

@auth_service.get("/health")
async def health_check():
    return {"status": "healthy"}