from transformers import pipeline



# Load Summarization model (will download the model on first run which will take some time and make sure to have internet connection)
print("Loading Summarization model...")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
print("Summarization model loaded successfully!")



def summarize_text(transcribe: str):
    """
    Summarizes a long text by splitting it into chunks.
    """
    print("Starting summarization...")
     # The model has a max input length. We need to chunk the text.
    max_chunk_length = 1000
    
    words = transcribe.split()
    chunks = [" ".join(words[i: i+max_chunk_length]) for i in range(0, len(words), max_chunk_length)]
    
    
    summaries = []    
    for chunk in chunks:
        summary = summarizer(chunk, max_length = 150, min_length = 30, do_sample = 50)
        summaries.append(summary[0]["summary_text"])
        
        
    final_summary = " ".join(summaries)
    print("Summarization completed!")
    return final_summary

