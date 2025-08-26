import os
import time
import asyncio
from google import genai
from config import GEMINI_API_KEY
import uuid

# Create the client with API key
client = genai.Client(api_key=GEMINI_API_KEY)

async def generate_video(prompt: str) -> str:
    """
    Generate a video using Google's Gemini Veo3 model
    
    Args:
        prompt: Text prompt describing the video to generate
        
    Returns:
        Path to the generated video file
    """
    try:
        # Create the videos directory if it doesn't exist
        os.makedirs("videos", exist_ok=True)
        
        # Start video generation operation
        operation = await asyncio.to_thread(
            client.models.generate_videos,
            model="veo-3.0-generate-preview",
            prompt=prompt,
        )
        
        # Poll the operation status until the video is ready
        while not operation.done:
            print("Waiting for video generation to complete...")
            await asyncio.sleep(10)  # Use asyncio.sleep in async functions
            operation = await asyncio.to_thread(client.operations.get, operation)
        
        # Generate a unique filename
        video_id = str(uuid.uuid4())
        video_path = os.path.join("videos", f"{video_id}.mp4")
        
        # Download the generated video
        generated_video = operation.response.generated_videos[0]
        await asyncio.to_thread(client.files.download, file=generated_video.video)
        
        # Save the video to our local path
        generated_video.video.save(video_path)
        print(f"Generated video saved to {video_path}")
        
        return video_path
    
    except Exception as e:
        print(f"Error generating video: {e}")
        raise
