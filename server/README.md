# AI Video Generation Service

A FastAPI-based service that generates videos from text prompts using state-of-the-art AI models with a Next.js frontend.

## Features

- Text-to-video generation using Hugging Face's text-to-video models
- Two-tier generation approach:
  - Primary: Cloud-based inference using Hugging Face Inference API
  - Fallback: Local generation using Diffusers library
- Asynchronous processing with background tasks
- RESTful API with status tracking

## Project Structure

```
peppo-task/
├── server/           # FastAPI backend
│   ├── utils/        # Utility modules
│   ├── videos/       # Generated videos storage
│   └── main.py       # Server entry point
└── client/           # Next.js frontend
    ├── components/   # React components
    ├── pages/        # Next.js pages
    ├── public/       # Static assets
    └── styles/       # CSS styles
```

## Backend (FastAPI)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Harsh-BH/peppo-task.git
cd peppo-task/server
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the server directory with your Hugging Face API token:
```
HF_TOKEN=your_huggingface_token_here
```

### Configuration

The application uses environment variables for configuration:

- `HF_TOKEN`: Your Hugging Face API token (required)

### Usage

1. Start the server:
```bash
python main.py
```

2. The server will be available at `http://localhost:8000`

### API Endpoints

#### Generate Video

```
POST /api/generate-video
```

Request body:
```json
{
  "prompt": "Astronaut in a jungle, cold color palette, muted colors, detailed, 8k"
}
```

Response:
```json
{
  "task_id": "12345-uuid",
  "status": "processing",
  "message": "Video generation started"
}
```

#### Check Video Status

```
GET /api/video-status/{task_id}
```

Response (processing):
```json
{
  "status": "processing"
}
```

Response (completed):
```json
{
  "status": "completed",
  "video_url": "/api/videos/12345-uuid"
}
```

Response (failed):
```json
{
  "status": "failed",
  "error": "Error message"
}
```

#### Download Generated Video

```
GET /api/videos/{task_id}
```

Returns the video file if generation is complete.

## Frontend (Next.js)

### Installation

1. Navigate to the client directory:
```bash
cd peppo-task/client
```

2. Install dependencies:
```bash
npm install
# or
yarn install
```

3. Create a `.env.local` file with the backend URL:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Development

Start the development server:
```bash
npm run dev
# or
yarn dev
```

The frontend will be available at `http://localhost:3000`.

### Building for Production

Build the frontend:
```bash
npm run build
# or
yarn build
```

Start the production server:
```bash
npm start
# or
yarn start
```

## Frontend Features

- Clean, responsive UI built with React and Next.js
- Real-time status updates for video generation
- Video preview with playback controls
- History of previously generated videos
- Form validation and error handling
- Mobile-friendly design

## Using the Web Interface

1. Open your browser and navigate to `http://localhost:3000`
2. Enter a detailed text prompt describing the video you want to generate
3. Click "Generate Video" to start the process
4. The interface will show the generation status in real-time
5. Once complete, the video will be displayed and available for download

## Architecture

The application uses a two-tier approach for video generation:

1. **Primary Method**: Uses Hugging Face's InferenceClient to generate videos using the cloud API. This requires an API key but offers better performance.

2. **Fallback Method**: If the primary method fails, the application falls back to local generation using the Diffusers library. This requires more computational resources but works without external dependencies.

All generation happens asynchronously in background tasks, allowing the API to respond quickly and clients to poll for status updates.

## Technologies Used

### Backend
- FastAPI: Web framework
- Hugging Face Hub: AI model access
- Diffusers: Local AI model execution
- Python 3.9+
- PyTorch: Deep learning framework
- Uvicorn: ASGI server

### Frontend
- Next.js: React framework
- React: UI library
- Tailwind CSS: Styling
- Axios: API requests
- React Query: Data fetching and caching
- React Player: Video playback

## Requirements

- Node.js 14+ (for frontend)
- Python 3.9+ (for backend)
- For local generation: GPU with CUDA support (recommended)

## Deployment

### Backend
The FastAPI backend can be deployed using Docker or directly on a server with Python installed. For production use, consider using Gunicorn with Uvicorn workers.

### Frontend
The Next.js frontend can be deployed to Vercel, Netlify, or any hosting service that supports Next.js applications.

Make sure to update the `NEXT_PUBLIC_API_URL` environment variable to point to your deployed backend API.
