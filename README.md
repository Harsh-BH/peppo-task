

# AI Video Generation Service

A FastAPI-based service that generates videos from text prompts using multiple AI video generation services (Hugging Face, Runway, Stability AI) with a local fallback and a Next.js frontend.

---

## Features

* Text-to-video generation using multiple AI services
* Multi-tier generation approach:

  * **Primary**: Hugging Face Inference API
  * **Secondary**: Runway API
  * **Tertiary**: Stability AI API
  * **Fallback**: Local generation using Diffusers library
* Asynchronous processing with background tasks
* RESTful API with status tracking

---

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

---

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

3. Create a `.env` file in the server directory with your API keys:

```
HF_TOKEN=your_huggingface_token_here
RUNWAY_API_KEY=your_runway_api_key_here
STABILITY_API_KEY=your_stability_api_key_here
```

---

### Configuration

The application uses environment variables for configuration:

* `HF_TOKEN`: Hugging Face API token
* `RUNWAY_API_KEY`: Runway API key
* `STABILITY_API_KEY`: Stability AI API key

---

### Usage

1. Start the server:

```bash
python main.py
```

2. The server will be available at `http://localhost:8000`

---

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

---

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

---

#### Download Generated Video

```
GET /api/videos/{task_id}
```

Returns the video file if generation is complete.

---

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

---

### Development

Start the development server:

```bash
npm run dev
# or
yarn dev
```

Frontend available at `http://localhost:3000`.

---

### Building for Production

```bash
npm run build
npm start
```

---

## Frontend Features

* Clean, responsive UI with React and Next.js
* Real-time status updates
* Video preview with playback controls
* History of generated videos
* Form validation and error handling
* Mobile-friendly design

---

## Architecture

The application uses a multi-tier approach for video generation:

1. **Primary Method** – Hugging Face Inference API
   High-performance cloud inference using state-of-the-art models.

2. **Secondary Method** – Runway API
   Used when Hugging Face inference fails.

3. **Tertiary Method** – Stability AI API
   Used if both Hugging Face and Runway fail.

4. **Fallback Method** – Local Diffusers library
   Used if all cloud services fail. Requires a GPU for optimal performance.

All generation happens asynchronously, allowing quick API responses while clients poll for updates.

---

## Technologies Used

### Backend

* FastAPI
* Hugging Face Hub
* Runway API
* Stability AI API
* Diffusers
* PyTorch
* Uvicorn

### Frontend

* Next.js
* React
* Tailwind CSS
* Axios
* React Query
* React Player

---

## Requirements

* Node.js 14+ (frontend)
* Python 3.9+ (backend)
* GPU with CUDA (for local generation)

---

## Deployment

Backend: Deploy via Gunicorn,AWS Ec2.
Frontend: Deploy via Vercel.
