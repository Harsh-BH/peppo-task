export interface VideoRequest {
  prompt: string;
}

export interface VideoResponse {
  task_id: string;
  status: string;
  message: string;
}

export interface VideoStatus {
  status: 'processing' | 'completed' | 'failed';
  video_url?: string;
  error?: string;
}

export const generateVideo = async (prompt: string): Promise<VideoResponse> => {
  const response = await fetch('/api/generate-video', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ prompt }),
  });

  if (!response.ok) {
    throw new Error('Failed to generate video');
  }

  return response.json();
};

export const getVideoStatus = async (taskId: string): Promise<VideoStatus> => {
  const response = await fetch(`/api/video-status/${taskId}`);

  if (!response.ok) {
    throw new Error('Failed to get video status');
  }

  return response.json();
};

export const getVideoUrl = (taskId: string): string => {
  return `/api/videos/${taskId}.mp4`;
};
