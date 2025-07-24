# app/main.py

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from pydantic import BaseModel
import logging
import uuid
import os

from app.prompt_generator import create_ad_prompt
from app.image_generator import generate_image
from app.utils import download_image

# Initialize app and logger
app = FastAPI()
logger = logging.getLogger("uvicorn.error")

# Create output directory if it doesn't exist
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Define request schema
class RequestPayload(BaseModel):
    product: str
    audience: str

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.warning(f"HTTP {exc.status_code}: {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError):
    logger.warning("Validation Error: %s", exc.errors())
    return JSONResponse(status_code=422, content={"errors": exc.errors()})

@app.exception_handler(Exception)
async def catch_all_handler(request: Request, exc: Exception):
    logger.error("Unhandled error: %s", exc)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

# Endpoint
@app.post("/generate")
def generate_ad_image(payload: RequestPayload):
    try:
        prompt = create_ad_prompt(payload.product, payload.audience)
        print("Generated Prompt:", prompt)

        image_url = generate_image(prompt)
        print("Image URL:", image_url)

        return {"prompt": prompt, "image_url": image_url}

    except HTTPException as http_err:
        print(f"HTTP Error {http_err.status_code}: {http_err.detail}")
        raise http_err

    except Exception as e:
        print(f"🔥 Unexpected Error: {e}")
        status = getattr(e, "status_code", 500) if hasattr(e, "status_code") else 500
        raise HTTPException(status_code=status, detail=str(e))