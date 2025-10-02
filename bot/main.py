import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from dotenv import load_dotenv
import httpx

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"), override=True)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is not set. Create bot/.env from bot/.env.example")

LEVEL_CHANNELS = {
    1: os.getenv("CHANID_LIV1"),
    2: os.getenv("CHANID_LIV2"),
    3: os.getenv("CHANID_LIV3"),
    4: os.getenv("CHANID_LIV4"),
}

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Benvenuto! Questo è il bot di notifica. Usa /health per verificare il backend, /register per registrarti, /my_level per vedere il tuo livello attuale.")

@dp.message(Command("health"))
async def health(message: Message):
    url = f"{API_BASE_URL}/api/health"
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.get(url)
            r.raise_for_status()
            data = r.json()
        await message.answer(f"Backend status: {data}")
    except Exception as e:
        await message.answer(f"Errore nel chiamare il backend: {e}")

@dp.message(Command("register"))
async def register(message: Message):
    args = message.text.split()
    level = 1
    if len(args) > 1 and args[1].isdigit():
        level = int(args[1])
        if level not in [1, 2, 3, 4]:
            await message.answer("Livello non valido. Scegli tra 1, 2, 3, 4.")
            return

    payload = {
        "telegram_id": message.from_user.id,
        "first_name": message.from_user.first_name,
        "last_name": message.from_user.last_name,
        "level": level,
    }
    url = f"{API_BASE_URL}/api/users/register_user"
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.post(url, json=payload)
            r.raise_for_status()
            data = r.json()
        status = data.get("status")
        response_text = f"Registrazione completata con successo! Il tuo stato è: {status}."
        invite_lines = []
        for l in range(1, level + 1):
            ch_id = LEVEL_CHANNELS.get(l)
            if ch_id:
                try:
                    inv_link = await bot.export_chat_invite_link(ch_id)
                    invite_lines.append(f"Livello {l}: {inv_link}")
                except Exception as e:
                    invite_lines.append(f"Livello {l}: Errore nel generare link - {str(e)}")
            else:
                invite_lines.append(f"Livello {l}: Canale non configurato")
        if invite_lines:
            response_text += "\nLink per unirti ai canali:\n" + "\n".join(invite_lines)
        else:
            response_text += "\nNessun canale disponibile."
        await message.answer(response_text)
    except httpx.HTTPStatusError as e:
        await message.answer(f"Errore durante la registrazione: {e.response.text}")
    except Exception as e:
        await message.answer(f"Errore durante la registrazione: {e}")

@dp.message(Command("channels"))
async def channels(message: Message):
    response_text = "Canali configurati:\n"
    for level, channel_id in LEVEL_CHANNELS.items():
        response_text += f"Livello {level}: {channel_id or 'Non configurato'}\n"
    await message.answer(response_text)

@dp.message(Command("my_level"))
async def my_level(message: Message):
    telegram_id = message.from_user.id
    url = f"{API_BASE_URL}/api/users/{telegram_id}"
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.get(url)
            r.raise_for_status()
            data = r.json()
        level = data.get("level", 0)
        status = data.get("status", "unknown")
        if status != "active":
            await message.answer("Il tuo account non è attivo.")
            return
        response_text = f"Il tuo livello attuale è {level}."
        invite_lines = []
        for l in range(1, level + 1):
            ch_id = LEVEL_CHANNELS.get(l)
            if ch_id:
                try:
                    inv_link = await bot.export_chat_invite_link(ch_id)
                    invite_lines.append(f"Livello {l}: {inv_link}")
                except Exception as e:
                    invite_lines.append(f"Livello {l}: Errore nel generare link - {str(e)}")
            else:
                invite_lines.append(f"Livello {l}: Canale non configurato")
        if invite_lines:
            response_text += "\nLink per unirti ai canali:\n" + "\n".join(invite_lines)
        else:
            response_text += "\nNessun canale disponibile."
        await message.answer(response_text)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            await message.answer("Utente non trovato. Usa /register per registrarti.")
        else:
            await message.answer(f"Errore durante la richiesta: {e.response.text}")
    except Exception as e:
        await message.answer(f"Errore: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
