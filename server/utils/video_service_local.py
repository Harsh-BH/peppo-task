import os
import asyncio
import uuid
import torch
from diffusers import DiffusionPipeline

# Initialize the model lazily to avoid loading it on import
pipe = None

def get_pipeline():
    global pipe
    if pipe is None:
        print("Loading diffusion model...")
        pipe = DiffusionPipeline.from_pretrained("Wan-AI/Wan2.1-T2V-1.3B-Diffusers")
        if torch.cuda.is_available():
            pipe = pipe.to("cuda")
        else:
            print("CUDA not available, using CPU. This may be slow.")
    return pipe

async def generate_video_local(prompt: str) -> str:
    try:
        os.makedirs("videos", exist_ok=True)
        
        video_id = str(uuid.uuid4())
        video_path = os.path.join("videos", f"{video_id}.mp4")
        
        print(f"Generating video locally with prompt: {prompt}")
        
        # Run the model in a separate thread to not block the event loop
        def run_inference():
            model = get_pipeline()
            output = model(prompt)
            # Save the first video from the output
            output.videos[0].save(video_path)
        
        await asyncio.to_thread(run_inference)
        
        print(f"Generated video saved to {video_path}")
        return video_path
    
    except Exception as e:
        print(f"Error generating video locally: {e}")
        raise
