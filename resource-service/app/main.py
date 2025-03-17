from fastapi import FastAPI
import os

resource_service = FastAPI()

@resource_service.post("/allocate_resources")
async def allocate_resources(request: dict):
    stress_cpu(2, request.get("load_factor", 1))
    stress_ram(2, request.get("load_factor", 1))
    return {"status": "resources_allocated"}

@resource_service.get("/health")
async def health_check():
    return {"status": "healthy"}