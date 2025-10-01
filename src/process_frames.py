from PIL import Image
import base64
import io
from dotenv import load_dotenv
from pathlib import Path
import argparse
from common_functions import update_stage
from frame_similarity import get_similarity
from db_functions import DB

VIDEO_PATH = "video"
MOVE_THRESHOLD = 0.95
SCENE_THRESHOLD = 0.8

load_dotenv()

def main(id: str):
    folder = Path(f"{VIDEO_PATH}/{id}/frames")
    files = list(folder.glob("*.png"))

    keyframes = [files[0]]
    for i, file in enumerate(files):
        print(f"\rProcessing frame: {i}/{len(files)} | Keyframes: {len(keyframes)}", end='', flush=True)
        similarity = get_similarity(keyframes[-1].as_posix(), file.as_posix())
        if similarity < SCENE_THRESHOLD:
            keyframes.append(file)
            timestamp = float(file.stem.split("t")[-1])
            upload_scene_frame(id, timestamp)
        elif similarity < MOVE_THRESHOLD:
            keyframes.append(file)
            timestamp = float(file.stem.split("t")[-1])
            upload_move_frame(id, timestamp)

    update_stage(id, "keyframes_extracted")

def upload_scene_frame(video_id: str, timestamp: float):
    db = DB(video_id)
    db.add_keyframe(timestamp, "scene")

def upload_move_frame(video_id: str, timestamp: float):
    db = DB(video_id)
    db.add_keyframe(timestamp, "move")

def encode_image_as_base64(path: str) -> str:
    with Image.open(path) as img:
        buffered = io.BytesIO()
        fmt = img.format or Path(path).suffix[1:]
        img.save(buffered, format=fmt.upper())
        img_b64 = base64.b64encode(buffered.getvalue()).decode()
        mime = f"image/{fmt.lower()}"
        return f"data:{mime};base64,{img_b64}"
   
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process frames")

    parser.add_argument(
        "--video-id",
        type=str,
        required=True,
        help="The id (generally a hex string) of the downloaded video to process."
    )

    args = parser.parse_args()

    main(args.video_id)