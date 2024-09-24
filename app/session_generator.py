# app/session_generator.py
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

async def generate_session_string(api_id, api_hash, phone, code):
    client = TelegramClient(StringSession(), api_id, api_hash)
    await client.connect()
    await client.sign_in(phone, code)
    return client.session.save()
