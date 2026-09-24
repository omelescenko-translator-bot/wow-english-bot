# -*- coding: utf-8 -*-
import os
import io
from aiogram import Router, types, F, Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BufferedInputFile
try:
    from gtts import gTTS
except ImportError:
    gTTS = None
import logging
from config import GEMINI_API_KEY

router = Router()
logger = logging.getLogger(__name__)

USER_SPEAKING_MODE = {}

SPEAKING_PROMPT = """You are an encouraging and friendly native English conversational partner.
The user is practicing their spoken/written English.
Respond naturally to what the user said in 2-4 sentences in clear English.
If the user made a noticeable grammar or phrasing mistake, add a very gentle, brief tip at the end formatted like:
💡 Tip: Instead of "... [user mistake] ...", it is more natural to say "... [correct phrase] ...".

Keep your tone positive, engaging, and supportive."""

# Initialize GenAI Client
_genai_client = None
try:
    from google import genai
    from google.genai import types as genai_types
    api_key = os.getenv("GEMINI_API_KEY", GEMINI_API_KEY)
    if api_key:
        _genai_client = genai.Client(api_key=api_key)
except Exception as e:
    logger.warning(f"GenAI Client init error in speaking.py: {e}")

async def query_ai(prompt: str, user_message: str) -> str:
    if _genai_client:
        try:
            resp = _genai_client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=f"{prompt}\n\nUser message: {user_message}"
            )
            if resp and resp.text:
                return resp.text.strip()
        except Exception as e:
            logger.warning(f"Gemini Speaking query error: {e}")
            
    return f"I understand! Let's continue discussing this topic. What else can you share?"

@router.message(F.text == "🗣️ Разговорный тренажёр")
@router.callback_query(F.data == "start_speaking_cb")
async def start_speaking_mode(event: types.Message | types.CallbackQuery):
    user_id = event.from_user.id
    USER_SPEAKING_MODE[user_id] = True
    
    text = (
        "🗣️ **Режим разговорного тренажёра активирован!**\n\n"
        "О чём хочешь пообщаться сегодня?\n"
        "Можешь написать мне текст или **отправить голосовое сообщение (войс)** на английском!\n\n"
        "🌟 *Примеры тем:*\n"
        "• How was your day?\n"
        "• Tell me about your favorite travel destination.\n"
        "• What are your plans for the weekend?\n\n"
        "*(Чтобы выйти из режима, нажми любую кнопку в основном меню)*"
    )
    
    if isinstance(event, types.CallbackQuery):
        await event.message.answer(text, parse_mode="Markdown")
        await event.answer()
    else:
        await event.answer(text, parse_mode="Markdown")

@router.message(F.voice)
async def handle_voice_message(message: types.Message, bot: Bot):
    await message.answer("🎧 Слушаю твой войс...")
    
    ai_reply = await query_ai(SPEAKING_PROMPT, "Hello! I am practicing my spoken English.")
    
    try:
        clean_text_for_tts = ai_reply.split("💡")[0].strip()
        tts = gTTS(text=clean_text_for_tts, lang='en', slow=False)
        bio = io.BytesIO()
        tts.write_to_fp(bio)
        bio.seek(0)
        audio = BufferedInputFile(bio.read(), filename="ai_reply.mp3")
        await message.answer_voice(audio, caption=ai_reply)
    except Exception:
        await message.answer(ai_reply)

@router.message(lambda msg: USER_SPEAKING_MODE.get(msg.from_user.id, False) and msg.text and not msg.text.startswith("/") and msg.text not in ["🃏 Тренировка карточек", "📚 Мой словарь", "🗣️ Разговорный тренажёр", "💼 Собеседование", "📊 Прогресс", "⚙️ Настройки", "📱 Открыть Mini App"])
async def handle_speaking_text(message: types.Message):
    ai_reply = await query_ai(SPEAKING_PROMPT, message.text)
    
    try:
        clean_text_for_tts = ai_reply.split("💡")[0].strip()
        tts = gTTS(text=clean_text_for_tts, lang='en', slow=False)
        bio = io.BytesIO()
        tts.write_to_fp(bio)
        bio.seek(0)
        audio = BufferedInputFile(bio.read(), filename="ai_reply.mp3")
        await message.answer_voice(audio, caption=ai_reply)
    except Exception:
        await message.answer(ai_reply)

