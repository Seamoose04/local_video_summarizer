import requests
from PIL import Image
import base64
import io
import os
os.environ.pop("SSL_CERT_FILE", None)
from dotenv import load_dotenv
from pathlib import Path
import argparse
from supabase import create_client
import json
from common_functions import update_json_stage
import uuid

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL", ""), os.getenv("SUPABASE_KEY", ""))

def main(id: str):
    folder = Path(f"video/{id}/frames")
    with open(f"video/{id}/details.json", "r") as f:
        video_details = json.load(f)

    files = list(folder.glob("*.png"))

    for i, file in enumerate(files):
        print(f"\rProcessing frame {i}/{len(files)}", end='', flush=True)
        description = get_image_caption_from_ollama(file.as_posix())
        timestamp = float(file.stem.split("t")[-1])
        upload_frame_summary(id, video_details["url"], timestamp, description)

    update_json_stage(f"video/{id}/details.json", "images_processed")

def upload_frame_summary(video_id: str, video_url: str, timestamp: float, description: str):
    frame_id = str(uuid.uuid4())
    result = supabase.table("video_summary_frames").insert({
        "id": frame_id,
        "video_url": video_url,
        "timestamp": timestamp,
        "frame_description": description
    }).execute()
    return result

def encode_image_as_base64(path: str) -> str:
    with Image.open(path) as img:
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()

def get_image_caption_from_ollama(image_path: str):
    b64_image = encode_image_as_base64(image_path)
    response = requests.post(f"{os.getenv("OLLAMA_BASE_URL")}/api/generate", json={
        "model": os.getenv("OLLAMA_MODEL"),
        "prompt": "Describe this image briefly.",
        "images": [b64_image],
        "stream": False
    })
    result = response.json()
    return result["response"].strip()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process frames")

    parser.add_argument(
        "--video_id",
        type=str,
        required=True,
        help="The id (generally a hex string) of the downloaded video to process."
    )

    args = parser.parse_args()

    main(args.video_id)