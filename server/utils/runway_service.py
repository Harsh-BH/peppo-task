import os
import asyncio
import uuid
import requests
import time
from config import RUNWAY_API_KEY

async def generate_video_runway(prompt: str) -> str:

    try:
        os.makedirs("videos", exist_ok=True)
        
        video_id = str(uuid.uuid4())
        video_path = os.path.join("videos", f"{video_id}.mp4")
        
        print(f"Generating video with Runway API. Prompt: {prompt}")
        
        def call_runway_api():
            headers = {
                "Authorization": f"Bearer {RUNWAY_API_KEY}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "prompt": prompt,
                "num_frames": 120,  # ~4 seconds at 30fps
                "fps": 30,
                "guidance_scale": 7.5,
                "motion_bucket_id": 40  # Controls the amount of motion
            }
            
            response = requests.post(
                "https://api.runwayml.com/v1/text-to-video/generations",
                headers=headers,
                json=payload
            )
            
            if response.status_code != 200:
                raise Exception(f"Runway API error: {response.text}")
            
            generation_id = response.json().get("id")
            
            max_attempts = 60
            for attempt in range(max_attempts):
                status_response = requests.get(
                    f"https://api.runwayml.com/v1/text-to-video/generations/{generation_id}",
                    headers=headers
                )
                
                if status_response.status_code != 200:
                    raise Exception(f"Runway API error checking status: {status_response.text}")
                
                status_data = status_response.json()
                status = status_data.get("status")
                
                if status == "SUCCEEDED":
                    video_url = status_data.get("output_url")
                    # Download the video
                    video_response = requests.get(video_url)
                    with open(video_path, "wb") as f:
                        f.write(video_response.content)
                    return video_path
                elif status == "FAILED":
                    raise Exception(f"Runway generation failed: {status_data.get('error', 'Unknown error')}")
                
                time.sleep(5)
            
            raise Exception("Runway generation timed out")
        
        return await asyncio.to_thread(call_runway_api)
        
    except Exception as e:
        print(f"Error generating video with Runway: {e}")
        raise
