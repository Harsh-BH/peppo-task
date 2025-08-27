import os
import time
import asyncio
from google import genai
from config import GEMINI_API_KEY
import uuid

client = genai.Client(api_key=GEMINI_API_KEY)

async def generate_video(prompt: str) -> str:

    try:
        os.makedirs("videos", exist_ok=True)
        
        operation = await asyncio.to_thread(
            client.models.generate_videos,
            model="veo-3.0-generate-preview",
            prompt=prompt,
        )
        
        while not operation.done:
            print("Waiting for video generation to complete...")
            await asyncio.sleep(10)  
            operation = await asyncio.to_thread(client.operations.get, operation)
        
        video_id = str(uuid.uuid4())
        video_path = os.path.join("videos", f"{video_id}.mp4")
        
        generated_video = operation.response.generated_videos[0]
        await asyncio.to_thread(client.files.download, file=generated_video.video)
        
        generated_video.video.save(video_path)
        print(f"Generated video saved to {video_path}")
        
        return video_path
    
    except Exception as e:
        print(f"Error generating video: {e}")
        raise
