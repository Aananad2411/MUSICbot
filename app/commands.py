from pyrogram import Client, filters
from app.config import BOT_NAME, OWNER_NAME
from app.player import join_and_play, pause_stream, resume_stream, stop_stream
from app.queue import add_to_queue, get_queue, get_next_track
import youtube_dl
import os

@Client.on_message(filters.command("alive"))
async def alive(_, message):
    await message.reply_text(f"**{BOT_NAME} is Alive!**\nOwned by: {OWNER_NAME}")

@Client.on_message(filters.command("ping"))
async def ping(_, message):
    import time
    start = time.time()
    msg = await message.reply("Pinging...")
    end = time.time()
    await msg.edit(f"🏓 Pong: `{round((end - start)*1000)} ms`")

@Client.on_message(filters.command("play"))
async def play_cmd(client, message):
    if len(message.command) < 2:
        return await message.reply("Please provide a song name or YouTube URL.")

    query = message.text.split(None, 1)[1]
    msg = await message.reply("🔎 Searching...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'quiet': True
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=True)
        audio_file = ydl.prepare_filename(info)

    chat_id = message.chat.id
    current_queue = get_queue(chat_id)

    if not current_queue:
        await msg.edit(f"🎶 Playing: {info['title']}")
        await join_and_play(chat_id, audio_file)
    else:
        await msg.edit(f"✅ Added to queue: {info['title']}")

    add_to_queue(chat_id, audio_file)

@Client.on_message(filters.command("queue"))
async def show_queue(_, message):
    q = get_queue(message.chat.id)
    if not q:
        return await message.reply("Queue is empty.")
    text = "**Current Queue:**\n"
    for i, track in enumerate(q, 1):
        name = os.path.basename(track).replace("_", " ")
        text += f"{i}. {name}\n"
    await message.reply(text)

@Client.on_message(filters.command("pause"))
async def pause_cmd(_, message):
    await pause_stream(message.chat.id)
    await message.reply("⏸️ Paused")

@Client.on_message(filters.command("resume"))
async def resume_cmd(_, message):
    await resume_stream(message.chat.id)
    await message.reply("▶️ Resumed")

@Client.on_message(filters.command("skip"))
async def skip_cmd(_, message):
    chat_id = message.chat.id
    next_track = get_next_track(chat_id)
    if next_track:
        await join_and_play(chat_id, next_track)
        await message.reply("⏭️ Skipped to next track.")
    else:
        await stop_stream(chat_id)
        await message.reply("🚫 Queue is empty. Left VC.")

@Client.on_message(filters.command("stop"))
async def stop_cmd(_, message):
    chat_id = message.chat.id
    from app.queue import clear_queue
    clear_queue(chat_id)
    await stop_stream(chat_id)
    await message.reply("🛑 Stopped and cleared queue.")
