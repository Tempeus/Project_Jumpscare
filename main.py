import random
from pathlib import Path
from moviepy import VideoFileClip, concatenate_videoclips

JUMPSCARE_PATH = './vids/'
JUMPSCARE_LIST = [VideoFileClip(vid) for vid in Path(JUMPSCARE_PATH).iterdir() if vid.is_file()]
MAX_OCCUR = 10 #Max number of occurrence of a single jumpscare
MIN_GAP = 1.0  # Minimum seconds between jumpscares (set to 0 for chaos)

# Pick a random jumpscare from the list by index - This function is called a random amount of time (0 - MAX_OCCUR?)
def pick_jumpscare() -> VideoFileClip:
    return random.choice(JUMPSCARE_LIST)

#TODO: Enhance this function - make sure there wont be multiple jumpscare happening at once? Actually, nested jumpscare would be pretty funny.
def insert_jumpscare(masterpiece: VideoFileClip, num_occurrences: int) -> list[VideoFileClip]:

    clips = []
    used_times = []

    duration = masterpiece.duration
    
    for _ in range(num_occurrences):
        jumpscare = pick_jumpscare()

        for _ in range(20):
            insert_time = random.uniform(0, duration - jumpscare.duration)
            if all(abs(insert_time - t) >= MIN_GAP for t in used_times):
                used_times.append(insert_time)
                break
            else:
                jumpscare.close()
                continue
        
        print(f"Inserting jumpscare at {insert_time:.2f}s")

        used_times.sort()

    current_time = 0.0

    for insert_time in used_times:
        clips.append(masterpiece.subclipped(current_time, insert_time))

        jumpscare = pick_jumpscare()
        clips.append(jumpscare)

        current_time = insert_time

    clips.append(masterpiece.subclipped(current_time, duration))

    return clips
    

def finalize(clip_list: list[VideoFileClip], output_path: str):
    final_clip = concatenate_videoclips(clip_list, method="compose")

    final_clip.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac"
    )

    # Cleanup
    final_clip.close()
    for clip in clip_list:
        clip.close()

if __name__ == "__main__":
    masterpiece = VideoFileClip("masterpiece.mp4")

    clip_list = insert_jumpscare(
        masterpiece,
        num_occurrences=MAX_OCCUR
    )

    finalize(clip_list, "final_output.mp4")

    masterpiece.close()