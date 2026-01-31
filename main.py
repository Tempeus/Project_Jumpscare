import random
from pathlib import Path
from moviepy import VideoFileClip, concatenate_videoclips

JUMPSCARE_PATH = './vids/'
JUMPSCARE_LIST = [VideoFileClip(vid) for vid in Path(JUMPSCARE_PATH).iterdir() if vid.is_file()]
MAX_OCCUR = 1 #Max number of occurrence of a single jumpscare

# Pick a random jumpscare from the list by index - This function is called a random amount of time (0 - MAX_OCCUR?)
def pick_jumpscare() -> VideoFileClip:
    idx_jumpscare = random.uniform(0,len(JUMPSCARE_LIST) - 1)
    return JUMPSCARE_LIST[idx_jumpscare]

#TODO: Enhance this function - make sure there wont be multiple jumpscare happening at once? Actually, nested jumpscare would be pretty funny.
def insert_jumpscare(masterpiece, jumpscare) -> list[VideoFileClip]:

    clip_list = []
    #Find where to put jumpscare
    max_start_time = masterpiece.duration
    insert_time = random.uniform(0, max_start_time)

    #TODO: Perform recursion on masterpiece until there are no longer any jumpscare to add?
    #Inserting the jumpscare
    print(f"Inserting clip at {insert_time:.2f} seconds")
    before = masterpiece.subclipped(0, insert_time)
    after = masterpiece.subclipped(insert_time, max_start_time)

    #combining the clips - how about we call concatenate_videoclips once, but the array is randomly generated.
    return clip_list

def finalize(clip_list, output_path):
    masterpiece = concatenate_videoclips(
        clip_list,
        method="compose"
    )

    masterpiece.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac"
    )

    masterpiece.close()

if __name__ == "__main__":
    masterpiece = VideoFileClip("masterpiece.mp4")

    #Refactor this
    for i in range(MAX_OCCUR):
        masterpiece = insert_jumpscare(masterpiece, pick_jumpscare)
    
    finalize()