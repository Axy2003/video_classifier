import os
import time
from typing import Any

import whisper
from moviepy import VideoFileClip

def transcribe_video(video_path: str):
    """
    Extracts audio from a video file and transcribes it using Whisper.
    """
    
    print("Starting the transcription process...")
    
    if not os.path.exists(video_path):
        return f"Video file not found at {video_path}"
    
    """Loading Whisper model"""
    # Load Summarization model (will download the model on first run which will take some time and make sure to have internet connection)
    print("Loading whisper 'base.en' model.....")
    model = whisper.load_model("base.en", device="cpu")
    print("Model Loaded successfully")
    
    
    try:
        video_clip = VideoFileClip(video_path)
        audio_path = r"temp_assets/temp_audio.wav"
        print(f"video fps {video_clip.fps}")
        if video_clip.audio:
            video_clip.audio.write_audiofile(audio_path)
        else:
            print("This video has no audio track.")
        # video_clip.audio.write_audiofile(audio_path)
        video_clip.close();
        print(f"Audio extracted and saved to {audio_path}")
        
    except Exception as e:
        return f"Error extracting audio: {e}"
        
        
    print("Transcribing audio...")
    start_time = time.time()
    result: dict[str, Any] = model.transcribe(audio_path)
    end_time = time.time()
    print(f"Transciption completed. Time taken: {end_time-start_time: .2f}secs")
    
    os.remove(audio_path)
    
    return {"transcription": str(result["text"])}


# uncomment the below code to run this file individually to check the output
# if __name__ == "__main__":
#     # Provide the video path of the file
#     video_file = r"C:\Users\Admin\Downloads\Top Headlines At 7 AM _ Ananya Panday Summoned For Third Time Today _ October 25, 2021.mp4"
    
    
#     transcription = transcribe_video(video_file)
    
#     print(transcription)