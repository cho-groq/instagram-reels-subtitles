"""
This recieves the POST request from the frontend and calls the appropriate functions and returns the captioned video + transcript

"""

def convert_mp4_to_mp3(mp4_filepath):
    """
    Converts an MP4 file to MP3.

    Args:
        mp4_filepath: Path to the input MP4 file.
        mp3_filepath: Path to save the output MP3 file.
    """
    video_clip = VideoFileClip(mp4_filepath)

    # Extract audio from video
    video_clip.audio.write_audiofile("../output.mp3")
    print("now is an mp3")
    video_clip.close()

# Step 1: Transcribe Audio
def transcribe_audio(mp3_file):

# Open the audio file
    with open(mp3_file, "rb") as file:
        # Create a transcription of the audio file
        transcription = client.audio.transcriptions.create(
            file=(mp3_file, file.read()), # Required audio file
            model="whisper-large-v3-turbo", # Required model to use for transcription
            # prompt="Specify context or spelling",  # Optional
            response_format="verbose_json",  # Optional
            language="en",  # Optional
            temperature=0.0  # Optional
        )
        # Print the transcription text
        # print(transcription.text)
        # print(transcription)
        return transcription.segments

    # model = whisper.load_model("small")  # Use 'tiny', 'base', 'small', 'medium', or 'large'
    # result = model.transcribe(video_path)
    # return result["segments"]

# Step 2: Convert to SRT Format
def convert_to_srt(segments, srt_path):
    subs = []
    for seg in segments:
        start = datetime.timedelta(seconds=seg["start"])
        end = datetime.timedelta(seconds=seg["end"])
        subs.append(srt.Subtitle(index=seg["id"], start=start, end=end, content=seg["text"]))
        print(start, end, "\n")

    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(srt.compose(subs))

# Step 3: Add Subtitles to Video
def add_subtitles(video_path, srt_path, output_path):
    video = mp.VideoFileClip(video_path)
    generator = lambda txt: mp.TextClip(txt, fontsize=24, color='white', bg_color='black')
    
    subtitles = SubtitlesClip(srt_path, generator)
    final_video = mp.CompositeVideoClip([video, subtitles.set_position(("center", "bottom"))])
    
    final_video.write_videofile(output_path, codec="libx264", fps=video.fps)

# Run the Process
video_file = "../input.mp4"
srt_file = "../subtitles.srt"
output_file = "output_with_subtitles.mp4"

mp3_file = "../output.mp3"
convert_mp4_to_mp3(video_file)
segments = transcribe_audio(mp3_file)
convert_to_srt(segments, srt_file)
add_subtitles(video_file, srt_file, output_file)

print("Subtitled video saved as:", output_file)
