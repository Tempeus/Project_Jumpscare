import random
from moviepy import VideoFileClip, concatenate_videoclips

vid_path = './vids/'

def insert_random_jumpscare(og_path, scare_path, output_path):
    og = VideoFileClip(og_path)
    jumpscare = VideoFileClip(scare_path)

    #Find where to put jumpscare
    max_start_time = og.duration
    insert_time = random.uniform(0, max_start_time)

    #Inserting the jumpscare
    print(f"Inserting clip at {insert_time:.2f} seconds")
    before = og.subclipped(0, insert_time)
    after = og.subclipped(insert_time, og.duration)

    #combining the clips
    masterpiece = concatenate_videoclips(
        [before, jumpscare, after],
        method="compose"
    )

    masterpiece.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac"
    )

    og.close()
    jumpscare.close()
    masterpiece.close()


if __name__ == "__main__":
    insert_random_jumpscare(
        og_path = vid_path + "2.mp4",
        scare_path = vid_path + "1.mp4",
        output_path = "masterpiece.mp4"
    )
