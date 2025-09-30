import os
import requests
os.environ.pop("SSL_CERT_FILE", None)
from supabase import create_client
from dotenv import load_dotenv
from common_functions import url_to_id, update_json_stage
import argparse

# Load environment variables from .env
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
MODEL_NAME = "nomic-embed-text"

# Create Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def main(url: str, batch_size: int = 32):
    id = url_to_id(url)
    data = supabase.table("video_summary_frames") \
        .select("id, frame_description") \
        .eq("video_url", url) \
        .is_("embedding", "null") \
        .execute().data
    
    update_json_stage(f"video/{id}/details.json", "retrieved_descriptions")

    total_batches = (len(data) + batch_size - 1) // batch_size

    # Step 3: Process in batches
    for i in range(0, len(data), batch_size):
        batch_index = i // batch_size + 1
        print(f"Processing batch {batch_index}/{total_batches}", end='\r')
        
        batch = data[i:i+batch_size]
        texts = [item["frame_description"] for item in batch]
        embeddings = embed_batch(texts)

        for item, vector in zip(batch, embeddings):
            supabase.table("frame_summaries").update({
                "embedding": vector
            }).eq("id", item["id"]).execute()
    
    update_json_stage(f"video/{id}/details.json", "embeddings_stored")

def embed_batch(texts):
    response = requests.post(f"{os.getenv("OLLAMA_BASE_URL")}/api/generate", json={
        "model": MODEL_NAME,
        "prompt": texts
    })
    result = response.json()
    print("DEBUG:", result)  # Add this to inspect structure
    if isinstance(result, list):
        return [r["embedding"] for r in result]
    else:
        return [result["embedding"]]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="embed frames to obtain vectors")

    parser.add_argument(
        "--url",
        type=str,
        required=True,
        help="The current video url"
    )

    parser.add_argument(
        "--batch_size",
        type=int,
        default=32,
        help="The number of descriptions to embed at once"
    )

    args = parser.parse_args()

    main(args.url, args.batch_size)