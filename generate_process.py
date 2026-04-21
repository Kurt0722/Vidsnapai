import os
import time
import subprocess
from text_to_audio import text_to_speech_file

def text_to_audio(folder):
    print("TTA -", folder)
    file_path = f"user_uploads/{folder}/desc.txt"

    if not os.path.exists(file_path):
        print(f"❌ desc.txt not found in {folder}")
        return False

    with open(file_path, "r") as f:
        text = f.read()

    text_to_speech_file(text, folder)

    # ✅ Check audio was actually created
    audio_path = f"user_uploads/{folder}/audio.mp3"
    if not os.path.exists(audio_path):
        print(f"❌ audio.mp3 was not generated for {folder}")
        return False

    return True

def create_reel(folder):
    print("CR -", folder)

    # ✅ Ensure output directory exists
    os.makedirs("static/reels", exist_ok=True)

    command = (
        f"ffmpeg -f concat -safe 0 "
        f"-i user_uploads/{folder}/input_files.txt "
        f"-i user_uploads/{folder}/audio.mp3 "
        f"-map 0:v -map 1:a "
        f"-vf \"scale=1080:1920:force_original_aspect_ratio=decrease,"
        f"pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black\" "
        f"-c:v libx264 -c:a aac -b:a 192k -shortest -r 30 -pix_fmt yuv420p "
        f"static/reels/reel_{folder}.mp4"  # ✅ unique name per folder
    )

    try:
        result = subprocess.run(command, shell=True, check=True,
                                capture_output=True, text=True)
        print(f"✅ Reel created for {folder}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ ffmpeg failed for {folder}:")
        print(e.stderr)  # ✅ now you'll actually see the error
        return False

if __name__ == "__main__":
    while True:
        with open("done.txt", "a+") as f:
            f.seek(0)
            done_folders = [line.strip() for line in f.readlines()]

        uploads_path = "user_uploads"
        if not os.path.exists(uploads_path):
            print(f"Folder '{uploads_path}' not found.")
            break

        folders = os.listdir(uploads_path)
        print("All folders:", folders)
        print("Done folders:", done_folders)

        for folder in folders:
            if folder not in done_folders:
                audio_ok = text_to_audio(folder)

                if not audio_ok:
                    print(f"⏭️ Skipping reel creation for {folder} — audio failed")
                    continue  # ✅ don't attempt reel without audio

                reel_ok = create_reel(folder)

                if reel_ok:  # ✅ only mark done if everything succeeded
                    with open("done.txt", "a") as f:
                        f.write(folder + "\n")

        time.sleep(5)