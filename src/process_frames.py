import requests
from PIL import Image
import base64
import io
import os
from dotenv import load_dotenv
from pathlib import Path
import argparse
from common_functions import update_stage
from lmstudio_functions import summarize_image
from db_functions import DB
import uuid

VIDEO_PATH = "video"

load_dotenv()

def main(id: str):
    folder = Path(f"{VIDEO_PATH}/{id}/frames")
    files = list(folder.glob("*.png"))

    for i, file in enumerate(files):
        print(f"\rProcessing frame {i}/{len(files)}", end='', flush=True)
        description = summarize_image(file.as_posix())
        timestamp = float(file.stem.split("t")[-1])
        upload_frame_summary(id, timestamp, description)

    update_stage(id, "images_processed")

def upload_frame_summary(video_id: str, timestamp: float, description: str):
    db = DB(video_id)

    db.upload_frame(timestamp, description)

def encode_image_as_base64(path: str) -> str:
    with Image.open(path) as img:
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()

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