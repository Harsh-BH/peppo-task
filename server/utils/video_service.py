import os
import asyncio
import uuid
from huggingface_hub import InferenceClient
from config import HF_TOKEN

async def generate_video(prompt: str, task_id: str) -> str:
    try:
        os.makedirs("videos", exist_ok=True)
        
        client = InferenceClient(
            provider="fal-ai",
            api_key=HF_TOKEN,
        )
        
        video_path = os.path.join("videos", f"{task_id}.mp4")
        
        print(f"Generating video with prompt: {prompt}")
        video = await asyncio.to_thread(
            client.text_to_video,
            prompt,
            model="Wan-AI/Wan2.2-T2V-A14B",
        )
        
        with open(video_path, "wb") as f:
            f.write(video)
        
        print(f"Generated video saved to {video_path}")
        return video_path
    
    except Exception as e:
        print(f"Error generating video: {e}")
        raise
