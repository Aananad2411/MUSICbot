# Anu Music Bot

A Telegram userbot that plays music in voice chats. Inspired by @MissQtBot.

## Features
- /play, /pause, /resume, /skip, /stop
- /ping, /alive
- Redis-based queue management
- Docker deployable

## Deployment
Add your .env variables and run:
```
docker build -t anu-music-bot .
docker run --env-file .env anu-music-bot
```
