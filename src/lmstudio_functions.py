from openai import OpenAI
import os
from dotenv import load_dotenv
import argparse
import re

load_dotenv()

LMSTUDIO_BASE_URL = os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234")
VISION_MODEL = os.getenv("VISION_MODEL", "")

# Point to LM Studio instead of OpenAI’s servers
client = OpenAI(base_url=f"{LMSTUDIO_BASE_URL}/v1", api_key="not-needed")

def remove_think_tags(text):
    pattern = r"\[THINK\].*?\[/THINK\]"
    cleaned_text = re.sub(pattern, "", text, flags=re.DOTALL)
    return cleaned_text

def summarize_image(img: str):
    response = client.chat.completions.create(
        model=VISION_MODEL,
        messages=[
            {"role": "user", "content": [
                {"type": "text", "text": "Describe this image briefly."},
                {"type": "image_url", "image_url": {"url": img}}
            ]}
        ],
        max_tokens=500
    )
    return remove_think_tags(response.choices[0].message.content) or ""

def summarize_changes(img1: str, img2: str):
    response = client.chat.completions.create(
        model=VISION_MODEL,
        messages=[
            {"role": "user", "content": [
                {"type": "text", "text": "Briefly describe the changes from the first image to the second, if there are any."},
                {"type": "image_url", "image_url": {"url": img1}},
                {"type": "image_url", "image_url": {"url": img2}}
            ]}
        ],
        max_tokens=500
    )
    return remove_think_tags(response.choices[0].message.content) or ""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Summarize image")

    parser.add_argument(
        "--img",
        type=str,
        required=True,
        help="The path of the image to summarize"
    )

    args = parser.parse_args()

    print("generating response...")
    from process_frames import encode_image_as_base64
    response = summarize_image(encode_image_as_base64(args.img))
    print(response)