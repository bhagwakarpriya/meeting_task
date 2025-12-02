import whisper

model = whisper.load_model("base")
result = model.transcribe(r"C:\Users\bhagw\Downloads\meeting_task\data\meeting.mp3")
# Get the text
transcript = result["text"]

# Save to a text file
with open(r"C:\Users\bhagw\Downloads\meeting_task\data\meeting.txt", "w", encoding="utf-8") as f:
    f.write(transcript)

print("Transcription saved to meeting.txt")
