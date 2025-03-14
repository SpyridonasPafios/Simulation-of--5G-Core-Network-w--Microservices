from fastapi import FastAPI
import os

session_service = FastAPI()

@session_service.post("/start_session")
async def start_session(request: dict):
    stress_cpu(3, request.get("load_factor", 1))
    stress_ram(3, request.get("load_factor", 1))
    return {"status": "session_started"}

@session_service.get("/health")
async def health_check():
    return {"status": "healthy"}