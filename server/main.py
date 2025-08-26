from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import os
from pydantic import BaseModel
# Updated import to use the new video_service module
from utils.video_service import generate_video
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
async def create_video(request: VideoRequest, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    tasks[task_id] = {"status": "processing", "video_path": None}
    
    background_tasks.add_task(
        process_video_generation, task_id, request.prompt
    )
    
    return VideoResponse(
        task_id=task_id,
        status="processing",
        message="Video generation started"
    )

async def process_video_generation(task_id: str, prompt: str):
    try:
        video_path = await generate_video(prompt)
        tasks[task_id] = {"status": "completed", "video_path": video_path}
    except Exception as e:
        tasks[task_id] = {"status": "failed", "error": str(e)}

@app.get("/api/video-status/{task_id}")
async def get_video_status(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = tasks[task_id]
    if task["status"] == "completed":
        return {"status": "completed", "video_url": f"/api/videos/{task_id}"}
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


