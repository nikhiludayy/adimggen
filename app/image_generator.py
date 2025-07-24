# app/image_generator.py

import openai
import os
from app.config import (
    AZURE_OPENAI_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_DEPLOYMENT_NAME,
    API_VERSION,
)

client = openai.AzureOpenAI(
    api_key=AZURE_OPENAI_KEY,
    api_version=API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
)

def generate_image(prompt: str) -> str:
    response = client.images.generate(
        model=AZURE_OPENAI_DEPLOYMENT_NAME,  # e.g., "dalle-3"
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    return response.data[0].url
