import os
import asyncio
import uuid
import requests
import time
from config import STABILITY_API_KEY

async def generate_video_stability(prompt: str) -> str:
    """
    Generate a video using Stability AI's API.
    
    Args:
        prompt (str): Text description of the video to generate
        
    Returns:
        str: Path to the generated video file
    """
    try:
        os.makedirs("videos", exist_ok=True)
        
        video_id = str(uuid.uuid4())
        video_path = os.path.join("videos", f"{video_id}.mp4")
        
        print(f"Generating video with Stability AI. Prompt: {prompt}")
        
        # Run the API requests in a separate thread to avoid blocking
        def call_stability_api():
            headers = {
                "Authorization": f"Bearer {STABILITY_API_KEY}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            # API endpoint for text-to-video
            url = "https://api.stability.ai/v1/generation/stable-video-diffusion/text-to-video"
            
            # Request payload
            payload = {
                "text_prompts": [
                    {
                        "text": prompt,
                        "weight": 1.0
                    }
                ],
                "height": 576,
                "width": 1024,
                "output_format": "mp4",
                "cfg_scale": 7.5,
                "motion_bucket_id": 40,
                "frames": 24,
                "fps": 6
            }
            
            # Make the API request
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code != 200:
                raise Exception(f"Stability AI API error: {response.text}")
            
            # Parse the response
            response_data = response.json()
            
            # Get the video URL or base64 data depending on API response format
            if "artifacts" in response_data and len(response_data["artifacts"]) > 0:
                artifact = response_data["artifacts"][0]
                
                if "binary" in artifact:
                    # If the API returns a direct video (base64)
                    import base64
                    video_data = base64.b64decode(artifact["binary"])
                    with open(video_path, "wb") as f:
                        f.write(video_data)
                elif "url" in artifact:
                    # If the API returns a URL to download the video
                    video_url = artifact["url"]
                    video_response = requests.get(video_url)
                    with open(video_path, "wb") as f:
                        f.write(video_response.content)
                else:
                    raise Exception("No video data in response")
            else:
                raise Exception("No video data in response")
            
            return video_path
        
        # Execute in a separate thread
        return await asyncio.to_thread(call_stability_api)
        
    except Exception as e:
        print(f"Error generating video with Stability AI: {e}")
        raise
