import tempfile
import os
import time

from fastapi import FastAPI, UploadFile, File

from transcribe import transcribe_video # importing transcribe.py to use its function
from summarize import summarize_text


app = FastAPI()

@app.post("/transcribe/")
async def transcribe_video_endpoint(video: UploadFile = File()):
    """
    Endpoint to upload a video file and get its transcription.
    """
    
    # used this part from gpt 
    # resource link:- https://docs.python.org/3/library/tempfile.html#tempfile.NamedTemporaryFile
    with tempfile.NamedTemporaryFile(delete = False, suffix= "mp4") as temp_video:
        content = await video.read()
        temp_video.write(content)
        temp_video_path = temp_video.name
        print(f"Video uploaded and saved to temporary file: {temp_video_path}")
        
    full_transcription = transcribe_video(temp_video_path)
    # transcription = transcribe_video(video_file)
    
    os.remove(temp_video_path)
    
    if "error" in full_transcription:
        return full_transcription
    
    start_time = time.time()
    final_transcription = full_transcription["transcription"]
    summary = summarize_text(final_transcription)
    end_time = time.time()
    print(f"Time taken: {end_time-start_time: .2f}sec")
    
    
    return {
        "transcription": final_transcription,
        "summary": summary
    }