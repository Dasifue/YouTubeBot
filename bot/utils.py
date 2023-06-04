from pytube import YouTube
import logging
import os

logging.basicConfig(level=logging.INFO)
video_streams = lambda video: video.streams.filter(progressive=True, file_extension="mp4", type="video")
audio_streams = lambda video: video.streams.filter(only_audio=True)

def find_video(url: str):
    video = YouTube(url=url, use_oauth=True, allow_oauth_cache=True)
    if video.check_availability():
        raise Exception(f"{video} is not available!")
    if video.length > 600:
        raise Exception(f"{video} is too long")
    return video


def get_video_info(video: YouTube):
    title = video.title
    author = video.author
    length = video.length

    data = {
        "title": title,
        "author": author,
        "length": length,
    }

    return data
    

def find_resolutions(video: YouTube):
    videos = video_streams(video).order_by("resolution")
    resolutions = list(set([video.resolution for video in videos]))
    return resolutions


def download_video(video: YouTube, resolution: str):
    data = get_video_info(video)
    video = video_streams(video).get_by_resolution(resolution)

    video.download(
        output_path="downloads/",
        filename=f"{data['title']}.mp4",
    )


def download_audio(video: YouTube):
    data = get_video_info(video)
    auido = audio_streams(video).first()

    print(auido)
    auido.download(
        output_path="downloads/",
        filename=f"{data['title']}.mp3",
    )


def delete_file(file_path):
    os.delete_file(file_path)
