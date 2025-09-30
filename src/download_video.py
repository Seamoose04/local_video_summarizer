import subprocess
import argparse
import cv2
from pathlib import Path
import os
import sys
import json
from common_functions import update_json_stage, url_to_id

VIDEO_PATH = "../video"

def main(url: str, fps: int):
    id = url_to_id(url)

    video_folder = Path(f"{VIDEO_PATH}/{id}")
    video_folder.mkdir(parents=True, exist_ok=True)

    create_json_details_file(url, fps, id, f"{VIDEO_PATH}/{id}/details.json")

    download_video(url, f"{VIDEO_PATH}/{id}/video.mp4")
    update_json_stage(f"{VIDEO_PATH}/{id}/details.json", "video_downloaded")

    extract_frames_with_timestamps(f"{VIDEO_PATH}/{id}/video.mp4", fps, f"{VIDEO_PATH}/{id}/frames")
    update_json_stage(f"{VIDEO_PATH}/{id}/details.json", "frames_split")

def create_json_details_file(url: str, fps: int, id: str, path: str = f"{VIDEO_PATH}/details.json"):
    details_data = {
        "id": id,
        "url": url,
        "fps": fps,
        "stage": "start"
    }

    with open(path, "w") as f:
        json.dump(details_data, f, indent=2)

def download_video(url: str, output_path: str = f"{VIDEO_PATH}/video.mp4"):
    try:
        cmd = [
            sys.executable, "-m", "yt_dlp",
            "--quiet", "--no-warnings",
            "--merge-output-format", "mp4",
            "-f", "bestvideo[height<=720]+bestaudio/best[height<=720]",
            "-o", output_path,
            url
        ]
        result = subprocess.run(cmd, check=True)
        print("Video download completed.")
    except subprocess.CalledProcessError as e:
        print(f"yt-dlp failed: {e}")

def extract_frames_with_timestamps(video_path: str, fps: int, output_dir: str = f"{VIDEO_PATH}/frames"):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    cap = cv2.VideoCapture(video_path)
    input_fps = cap.get(cv2.CAP_PROP_FPS)
    if input_fps == 0:
        raise ValueError("Could not read video FPS. Invalid file?")

    frame_interval = int(round(input_fps / fps))
    frame_idx = 0
    saved_idx = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % frame_interval == 0:
            timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0  # in seconds
            filename = os.path.join(output_dir, f"frame_{saved_idx:06d}_t{round(timestamp, 3):06.3f}.png")
            cv2.imwrite(filename, frame)
            saved_idx += 1

        frame_idx += 1

    cap.release()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download a video for summarization.")

    parser.add_argument(
        "--fps",
        type=int,
        choices=range(1, 11),
        default=2,
        help="The framerate to download the video at. Lower framerates process faster, but may miss small details. range: 1-10"
    )

    parser.add_argument(
        "--url", 
        type=str, 
        required=True, 
        help="URL of the YouTube video to download"
    )

    args = parser.parse_args()
    main(args.url, args.fps)