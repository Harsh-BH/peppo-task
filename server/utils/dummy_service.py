import os
import asyncio
import uuid
import cv2
import numpy as np

async def generate_dummy_video(prompt: str, error_message: str = "Video generation failed") -> str:

    try:
        os.makedirs("videos", exist_ok=True)
        
        video_id = str(uuid.uuid4())
        video_path = os.path.join("videos", f"{video_id}.mp4")
        
        print(f"Generating dummy video for failed request. Prompt was: {prompt}")
        
        def create_dummy_video():
            width, height = 640, 480
            fps = 24
            duration = 5
            
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))
            
            for frame_idx in range(fps * duration):
                img = np.zeros((height, width, 3), dtype=np.uint8)
                
                cv2.rectangle(img, (100, 140), (width-100, 180), (0, 0, 200), -1)
                cv2.putText(img, error_message, (120, 165), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
                cv2.putText(img, "Your prompt:", (width//2 - 70, 220), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                
                prompt_wrapped = []
                words = prompt.split()
                line = ""
                for word in words:
                    if len(line + word) < 40:
                        line += word + " "
                    else:
                        prompt_wrapped.append(line)
                        line = word + " "
                if line:
                    prompt_wrapped.append(line)
                
                y_pos = 260
                for line in prompt_wrapped[:5]:
                    cv2.putText(img, line, (width//2 - 150, y_pos), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                    y_pos += 30
                
                cv2.putText(img, f"Frame {frame_idx+1}/{fps*duration}", (20, height-20), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 1)
                
                out.write(img)
            
            out.release()
            
            return video_path
        
        return await asyncio.to_thread(create_dummy_video)
        
    except Exception as e:
        print(f"Error generating dummy video: {e}")
        
        try:
            video_array = np.zeros((24, 480, 640, 3), dtype=np.uint8)
            
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(video_path, fourcc, 24, (640, 480))
            
            for frame in video_array:
                out.write(frame)
            
            out.release()
            return video_path
        except Exception as final_error:
            print(f"Last resort video creation failed: {final_error}")
            return video_path
