# Asynchronous Multimodal Video Summarizer

A powerful, asynchronous video analysis tool that generates a concise text summary and identifies key visual moments from a video file. Built with FastAPI, Celery, and a suite of modern AI/ML models.

-----

## 🚀 Features

  * **Asynchronous Processing**: Upload a video and get an instant response with a task ID. The heavy processing happens in the background, ensuring the API is always fast and responsive.
  * **Audio Transcription**: Uses OpenAI's Whisper model to generate a highly accurate, word-for-word transcript of the video's audio.
  * **Text Summarization**: Employs a Hugging Face Transformer model (BART) to create a concise, abstractive summary from the full transcript.
  * **Visual Scene Detection**: Analyzes video frames with OpenCV to detect significant visual changes (like slide changes in a presentation) and provides timestamps for these key moments.
  * **Robust & Scalable**: The distributed architecture with a message broker (Redis) and task queue (Celery) is designed for reliability and can be scaled to handle multiple concurrent jobs.

-----

## 🏛️ System Architecture

The application is built on a modern, distributed system architecture to efficiently handle long-running, resource-intensive tasks.

[Image of a distributed system architecture diagram]

1.  **FastAPI Server (The Waiter)**: The user interacts with this lightweight web server. It accepts the video upload, creates a job ticket, and sends it to Redis. It responds instantly with a `task_id`.
2.  **Redis (The Order System)**: An in-memory message broker that queues the jobs from the API and stores the final results.
3.  **Celery Worker (The Chef)**: A separate background process that continuously watches Redis. When a new job appears, it picks it up, performs all the heavy AI/ML processing (transcription, summarization, vision analysis), and posts the final result back to Redis.

-----

## 🛠️ Technology Stack

  * **Backend**: FastAPI
  * **Task Queue**: Celery
  * **Message Broker**: Redis
  * **Containerization**: Docker
  * **Speech-to-Text**: `openai-whisper`
  * **Summarization**: `transformers` (Hugging Face)
  * **Video Processing**: `moviepy`, `opencv-python`
  * **ML Framework**: PyTorch

-----

## ⚙️ Setup and Installation

Follow these steps to set up the project on your local machine.

### Prerequisites

  * Python 3.10+
  * Docker
  * **ffmpeg**: Make sure it's installed and available in your system's PATH.
      * **macOS**: `brew install ffmpeg`
      * **Ubuntu**: `sudo apt update && sudo apt install ffmpeg`
      * **Windows**: Download from the [official site](https://ffmpeg.org/download.html) and add the `bin` folder to your PATH.

### Installation Steps

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Create and install dependencies:**
    First, create a `requirements.txt` file by running this command in your activated virtual environment:

    ```bash
    pip freeze > requirements.txt
    ```

    Then, install the packages:

    ```bash
    pip install -r requirements.txt
    ```

-----

## ▶️ How to Run

You need to run three services in three separate terminals.

### Terminal 1: Start Redis

Navigate to the project directory and start the Redis container using Docker.

```bash
docker run -d -p 6379:6379 --name video-summarizer-redis redis
```

### Terminal 2: Start the Celery Worker

In a new terminal, activate the virtual environment and start the worker. It will automatically load the AI models.

```bash
celery -A celery_app.celery worker --loglevel=info -I transcribe,summarize,vision,combiner -P solo
```

### Terminal 3: Start the FastAPI Server

In a third terminal, activate the virtual environment and start the Uvicorn server.

```bash
uvicorn main:app --reload
```

The API is now live and accessible at `http://127.0.0.1:8000`.

-----

## 📡 API Endpoints

You can interact with the API via the auto-generated documentation at **`http://127.0.0.1:8000/docs`**.

### 1\. Submit a Video for Analysis

  * **Endpoint**: `POST /analyze-video`
  * **Request Body**: `multipart/form-data` with a video file.
  * **Successful Response (200 OK)**: Instantly returns a JSON object with the task ID.
    ```json
    {
      "task_id": "a1b2c3d4-e5f6-7890-a1b2-c3d4e5f67890"
    }
    ```

### 2\. Check the Result

  * **Endpoint**: `GET /results/{task_id}`
  * **Path Parameter**: The `task_id` from the previous step.
  * **Pending Response**:
    ```json
    {
      "status": "PENDING"
    }
    ```
  * **Successful Response**:
    ```json
    {
      "status": "SUCCESS",
      "result": {
        "summary": "This is a concise summary of the video content...",
        "transcription": "This is the full text transcription of everything spoken...",
        "key_moments": [0.0, 15.32, 45.1, 92.5]
      }
    }
    ```

-----

## 🔮 Future Work

  * **Containerize the full application** with Docker Compose for one-command startup.
  * **Build a simple frontend** to provide a user-friendly interface for uploads and results.
  * **Experiment with more advanced models** like Longformer to avoid manual text chunking.
  * **Add more visual intelligence**, such as on-screen text recognition (OCR) or object detection.
