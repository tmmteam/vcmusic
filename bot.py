# bot.py

import os
from pyrogram import Client, filters
from youtube_api import get_song
from queue_manager import (
    add_to_queue,
    get_next_song,
    view_queue,
    clear_queue,
    toggle_repeat,
)
from player import init_player, play_song, stop_song, pause_song, resume_song

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
STRING_SESSION = os.getenv("STRING_SESSION")

app = Client(
    "music_userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION
)


@app.on_message(filters.me & filters.command("play", prefixes="."))
async def play_handler(client, message):
    query = " ".join(message.command[1:])

    if not query:
        return await message.reply("Give a song name.")

    song = await get_song(query)

    if not song:
        return await message.reply("Song not found.")

    add_to_queue(song)

    if len(view_queue()) == 1:
        await play_song(message.chat.id, song["file_path"])

    await message.reply(
        f"Started streaming\n"
        f"Title: {song['title']}\n"
        f"Duration: {song['duration']}\n"
        f"Requested by: You\n\n"
        f"00:00 ▬▬▬▬▬▬🔘──────── 0:00"
    )


@app.on_message(filters.me & filters.command("skip", prefixes="."))
async def skip_handler(client, message):
    next_song = get_next_song()

    if next_song:
        await play_song(message.chat.id, next_song["file_path"])
        await message.reply(f"Skipped to: {next_song['title']}")
    else:
        await stop_song(message.chat.id)
        await message.reply("Queue ended.")


@app.on_message(filters.me & filters.command("pause", prefixes="."))
async def pause_handler(client, message):
    await pause_song(message.chat.id)
    await message.reply("Paused.")


@app.on_message(filters.me & filters.command("resume", prefixes="."))
async def resume_handler(client, message):
    await resume_song(message.chat.id)
    await message.reply("Resumed.")


@app.on_message(filters.me & filters.command("end", prefixes="."))
async def end_handler(client, message):
    clear_queue()
    await stop_song(message.chat.id)
    await message.reply("Playback ended.")


@app.on_message(filters.me & filters.command("queue", prefixes="."))
async def queue_handler(client, message):
    q = view_queue()

    if not q:
        return await message.reply("Queue is empty.")

    text = "\n".join([f"{i+1}. {song['title']}" for i, song in enumerate(q)])
    await message.reply(f"Queue:\n{text}")


@app.on_message(filters.me & filters.command("repeat", prefixes="."))
async def repeat_handler(client, message):
    state = toggle_repeat()
    await message.reply(f"Repeat mode: {'ON' if state else 'OFF'}")


async def main():
    await app.start()
    await init_player(app)
    print("Music Userbot Started")
    await idle()


if __name__ == "__main__":
    from pyrogram.idle import idle
    app.run(main())
