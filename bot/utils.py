from aiogram import types, exceptions
from pytube import YouTube
import logging
import os

logging.basicConfig(level=logging.INFO)
video_streams = lambda video: video.streams.filter(progressive=True, file_extension="mp4", type="video")
audio_streams = lambda video: video.streams.filter(only_audio=True)

def wrong_url(url: str) -> bool:
    return not url.startswith("https://www.youtube.com/watch?v=")


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

    return f"downloads/{data['title']}.mp4"


def download_audio(video: YouTube):
    data = get_video_info(video)
    auido = audio_streams(video).first()

    auido.download(
        output_path="downloads/",
        filename=f"{data['title']}.mp3",
    )

    return f"downloads/{data['title']}.mp3"


async def send_audio(message: types.Message, file_path: str):
    with open(file_path, "rb") as file:
        try:
            await message.reply_audio(file)
        except exceptions.NetworkError:
            await message.reply("Sorry! File too large for uploading")


async def send_video(message: types.Message, file_path: str):
    with open(file_path, "rb") as file:
        try:
            await message.reply_video(file)
        except exceptions.NetworkError:
            await message.reply("Sorry! File too large for uploading")

def delete_file(file_path):
    os.remove(file_path)
