from aiogram import types, exceptions, Bot
from pytube import YouTube
from dotenv import load_dotenv
import logging
import os

from ..database import get_message_author, get_message, ENGINE


load_dotenv(".env")

logging.basicConfig(level=logging.INFO)
video_streams = lambda video: video.streams.filter(progressive=True, file_extension="mp4", type="video")
audio_streams = lambda video: video.streams.filter(only_audio=True)

def wrong_url(url: str) -> bool:
    if url.startswith("https://www.youtube.com/watch?v=") or url.startswith("https://youtu.be"):
        return False
    return True

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
            await message.reply("Sorry! File too large for uploading. Try to use less resolution")


async def send_video(message: types.Message, file_path: str):
    with open(file_path, "rb") as file:
        try:
            await message.reply_video(file)
        except exceptions.NetworkError:
            await message.reply("Sorry! File too large for uploading")

def delete_file(file_path):
    os.remove(file_path)


async def send_answer(data):
    print(data)
    author = get_message_author(engine=ENGINE, message_id=data["message_id"])
    message = get_message(engine=ENGINE, message_id=data["message_id"])
    answer = data["answer"]
    text = f"""
    Hello! Here an answer of your message: 
    {message.text}

    {answer}
    """

    print(author)

    bot = Bot(os.getenv("BOT_TOKEN"))
    await bot.send_message(chat_id=author, text=text)



__all__ = [
    'wrong_url',
    'find_video',
    'find_resolutions',
    'download_video',
    'download_audio',
    'send_audio',
    'send_video',
    'delete_file',
    'send_answer',
]