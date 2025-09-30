from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

LMSTUDIO_BASE_URL = os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234")
VISION_MODEL = os.getenv("VISION_MODEL", "")

# Point to LM Studio instead of OpenAI’s servers
client = OpenAI(base_url=f"{LMSTUDIO_BASE_URL}/v1", api_key="not-needed")

def summarize_image(img_path: str):
    response = client.chat.completions.create(
        model=VISION_MODEL,
        messages=[
            {"role": "user", "content": [
                {"type": "text", "text": "Describe this image briefly."},
                {"type": "image_url", "image_url": {"url": img_path}}
            ]}
        ],
        max_tokens=500
    )
    return response.choices[0].message.content or ""