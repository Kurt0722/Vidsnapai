from gtts import gTTS
import os

def text_to_speech_file(text, folder):
    try:
        tts = gTTS(text=text, lang='en')

        output_path = f"user_uploads/{folder}/audio.mp3"
        tts.save(output_path)

        print("✅ Audio generated:", output_path)

    except Exception as e:
        print("❌ gTTS failed:", e)