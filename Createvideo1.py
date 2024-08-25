from moviepy.editor import AudioFileClip, VideoFileClip, ImageClip, concatenate_videoclips
import os
def concatenate(video_clip_paths, output_path, method="compose"):
    """Concatenates several video files into one video file
    and save it to `output_path`. Note that extension (mp4, etc.) must be added to `output_path`
    `method` can be either 'compose' or 'reduce':
        `reduce`: Reduce the quality of the video to the lowest quality on the list of `video_clip_paths`.
        `compose`: type help(concatenate_videoclips) for the info"""
    # create VideoFileClip object for each video file
    clips = [VideoFileClip(c) for c in video_clip_paths]
    if method == "reduce":
        # calculate minimum width & height across all clips
        min_height = min([c.h for c in clips])
        min_width = min([c.w for c in clips])
        # resize the videos to the minimum
        clips = [c.resize(newsize=(min_width, min_height)) for c in clips]
        # concatenate the final video
        final_clip = concatenate_videoclips(clips)
    elif method == "compose":
        # concatenate the final video with the compose method provided by moviepy
        final_clip = concatenate_videoclips(clips, method="compose")
    # write the output video file
    final_clip.write_videofile(output_path)

def stitch_video(save_path, audio_paths, image_paths):
    video_paths=[]
    n=0
    for v, i in zip(audio_paths, image_paths):
        audio_clip = AudioFileClip(v)  # Load the audio clip
        image_clip = ImageClip(i)
        image_clip = image_clip.set_duration(audio_clip.duration)  # Create an image clip with the same duration as the audio
        video = image_clip.set_audio(audio_clip)
        new_path=os.path.join(save_path,f"video_{n}.mp4")
        video_paths.append(new_path)
        video.write_videofile(new_path,codec='libx264',fps=24)
        n=n+1
    final_path=os.path.join(save_path,f"chunk_summaries.mp4")
    method="compose"
    concatenate(video_paths,final_path,method)
   

