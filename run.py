from pyrogram import Client
from app.config import API_ID, API_HASH, SESSION

app = Client(name="AnuMusicBot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)

from app import commands  # Load command handlers

app.run()
