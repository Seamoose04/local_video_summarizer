import argparse
from db_functions import DB
from lmstudio_functions import summarize_image, summarize_changes
from process_frames import encode_image_as_base64
from common_functions import update_stage
import glob
import os


def main(id: str):
    FRAME_PATH = f"video/{id}/frames"

    db = DB(id)
    keyframe = db.get_new_keyframe()

    if keyframe:
        print("Processing keyframes...")
        frame_id, ts, frame_type = keyframe
        frame_path = glob.glob(f"{FRAME_PATH}/frame_*_t{ts:06.3f}.png")[0]
        scene_root64 = encode_image_as_base64(frame_path)
        description = summarize_image(scene_root64)
        db.update_keyframe_description(frame_id, description)

        keyframe = db.get_new_keyframe()
        while keyframe:
            frame_id, ts, frame_type = keyframe
            frame_path = glob.glob(os.path.join(FRAME_PATH, f"frame_*_t{ts:06.3f}.png"))[0]
            frame64 = encode_image_as_base64(frame_path)

            print(f"\rProcessing keyframe: {frame_id}", end='', flush=True)
            
            description = ""
            if frame_type == "scene":
                description = summarize_image(frame64)
            elif frame_type == "move":
                description = summarize_changes(scene_root64, frame64)
            db.update_keyframe_description(frame_id, description)

            keyframe = db.get_new_keyframe()
    
    update_stage(id, "keyframes_processed")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process frames")

    parser.add_argument(
        "--video-id",
        type=str,
        required=True,
        help="The id (generally a hex string) of the video's frames to process."
    )

    args = parser.parse_args()

    main(args.video_id)