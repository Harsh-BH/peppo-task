from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import os
from pydantic import BaseModel
# Import all video generation methods
from utils.video_service import generate_video
from utils.runway_service import generate_video_runway
from utils.stability_service import generate_video_stability
from utils.video_service_local import generate_video_local
from utils.dummy_service import generate_dummy_video
import uvicorn
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("videos", exist_ok=True)

class VideoRequest(BaseModel):
    prompt: str

class VideoResponse(BaseModel):
    task_id: str
    status: str
    message: str

tasks = {}

@app.post("/api/generate-video", response_model=VideoResponse)
async def create_video(request: VideoRequest):
    task_id = str(uuid.uuid4())
    tasks[task_id] = {"status": "processing", "video_path": None}
    
    # Directly await the function instead of using background tasks
    await process_video_generation(task_id, request.prompt)
    
    # Get the updated task status after processing is complete
    task = tasks[task_id]
    
    if task["status"] == "completed":
        return VideoResponse(
            task_id=task_id,
            status="completed",
            message="Video generation completed"
        )
    else:
        return VideoResponse(
            task_id=task_id,
            status="failed",
            message=task.get("error", "Unknown error")
        )

async def process_video_generation(task_id: str, prompt: str):
    error_messages = []
    try:
        try:
            # Try the primary method first (huggingface_hub)
            video_path = await generate_video(prompt)
            tasks[task_id] = {"status": "completed", "video_path": video_path}
        except Exception as e:
            error_messages.append(f"Primary video generation failed: {e}")
            print(error_messages[-1])
            print("Falling back to Runway API method...")
            
            try:
                video_path = await generate_video_runway(prompt)
                tasks[task_id] = {"status": "completed", "video_path": video_path}
            except Exception as runway_error:
                error_messages.append(f"Runway video generation failed: {runway_error}")
                print(error_messages[-1])
                print("Falling back to Stability AI method...")
                
                try:
                    video_path = await generate_video_stability(prompt)
                    tasks[task_id] = {"status": "completed", "video_path": video_path}
                except Exception as stability_error:
                    error_messages.append(f"Stability AI video generation failed: {stability_error}")
                    print(error_messages[-1])
                    print("Falling back to local video generation method...")
                    
                    try:
                        video_path = await generate_video_local(prompt)
                        tasks[task_id] = {"status": "completed", "video_path": video_path}
                    except Exception as local_error:
                        error_messages.append(f"Local video generation failed: {local_error}")
                        print(error_messages[-1])
                        print("All generation methods failed. Creating dummy video...")
                        
                        # Final fallback - always provide some video response
                        combined_errors = "\n".join(error_messages)
                        video_path = await generate_dummy_video(prompt, f"All generation methods failed")
                        tasks[task_id] = {
                            "status": "completed", 
                            "video_path": video_path,
                            "is_fallback": True,
                            "error_details": combined_errors
                        }
    except Exception as e:
        tasks[task_id] = {"status": "failed", "error": str(e)}

@app.get("/api/video-status/{task_id}")
async def get_video_status(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = tasks[task_id]
    if task["status"] == "completed":
        response = {"status": "completed", "video_url": f"/api/videos/{task_id}"}
        if task.get("is_fallback"):
            response["is_fallback"] = True
            response["message"] = "All generation methods failed, showing fallback video"
        return response
    elif task["status"] == "failed":
        return {"status": "failed", "error": task.get("error", "Unknown error")}
    else:
        return {"status": "processing"}

@app.get("/api/videos/{task_id}")
async def get_video(task_id: str):
    if task_id not in tasks or tasks[task_id]["status"] != "completed":
        raise HTTPException(status_code=404, detail="Video not found")
    
    video_path = tasks[task_id]["video_path"]
    return FileResponse(video_path, media_type="video/mp4")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


