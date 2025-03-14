from fastapi import FastAPI
import os

policy_service = FastAPI()

@policy_service.post("/apply_policy")
async def apply_policy(request: dict):
    stress_cpu(4, request.get("load_factor", 1))
    stress_ram(2, request.get("load_factor", 1))
    return {"status": "policy_applied"}

@policy_service.get("/health")
async def health_check():
    return {"status": "healthy"}