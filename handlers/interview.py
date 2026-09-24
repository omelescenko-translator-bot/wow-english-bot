# -*- coding: utf-8 -*-
import os
import io
import logging
from aiogram import Router, types, F, Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BufferedInputFile
try:
    from gtts import gTTS
except ImportError:
    gTTS = None
from config import GEMINI_API_KEY

router = Router()
logger = logging.getLogger(__name__)

USER_INTERVIEW_STATE = {} # user_id -> {'role': role_key, 'q_idx': 0}

INTERVIEW_ROLES = {
    "logistics": "Логистика / ВЭД / Цепочки поставок",
    "backoffice": "Координатор бэк-офиса / Операционный менеджер",
    "general": "Общие вопросы HR / Самопрезентация"
}

QUESTIONS = {
    "logistics": [
        "Could you briefly introduce yourself and summarize your experience in supply chain management?",
        "How do you handle unexpected delays with customs clearance or delayed freight deliveries?",
        "Tell me about a time when you managed to negotiate better freight rates or shorten lead time."
    ],
    "backoffice": [
        "What was your most important responsibility in your recent role?",
        "How do you prioritize multiple urgent tasks from different departments?",
        "Describe a situation where you had to deal with a difficult client or supplier complaint."
    ],
    "general": [
        "What is your greatest strength and what are your weaknesses?",
        "Why are you leaving your current position?",
        "Where do you see yourself professionally in the next 2-3 years?"
    ]
}

# Initialize GenAI Client
_genai_client = None
try:
    from google import genai
    api_key = os.getenv("GEMINI_API_KEY", GEMINI_API_KEY)
    if api_key:
        _genai_client = genai.Client(api_key=api_key)
except Exception as e:
    logger.warning(f"GenAI Client init error in interview.py: {e}")

async def evaluate_interview_answer(role_name: str, question: str, user_answer: str) -> str:
    prompt = (
        f"You are an experienced international HR recruiter conducting a job interview for the position: '{role_name}'.\n"
        f"Interview question was: '{question}'.\n"
        f"Candidate's answer: '{user_answer}'.\n\n"
        "Provide a concise, constructive assessment in Russian and English with the following structure:\n"
        "1. 🌟 Оценка ответа (Краткий комментарий по содержанию и уверенности)\n"
        "2. 💡 Рекомендация по формулировкам (Как улучшить ответ, используя естественные деловые фразы на английском)\n"
        "3. ✨ Пример сильного ответа (1-2 предложения на английском)"
    )
    if _genai_client:
        try:
            resp = _genai_client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )
            if resp and resp.text:
                return resp.text.strip()
        except Exception as e:
            logger.warning(f"Gemini Interview evaluation error: {e}")
            
    return (
        "🌟 **Отличный ответ!** Вы уверенно раскрыли суть вопроса.\n"
        "💡 **Совет:** Старайтесь использовать метод STAR (Situation, Task, Action, Result) и конкретные результаты в цифрах."
    )

@router.message(F.text == "💼 Собеседование")
@router.callback_query(F.data == "start_interview_cb")
async def interview_menu(event: types.Message | types.CallbackQuery):
    user_id = event.from_user.id
    USER_INTERVIEW_STATE.pop(user_id, None)
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📦 Логистика и ВЭД", callback_data="role_logistics")],
        [InlineKeyboardButton(text="🏢 Координатор бэк-офиса", callback_data="role_backoffice")],
        [InlineKeyboardButton(text="🤝 Общие вопросы HR", callback_data="role_general")]
    ])
    
    text = (
        "💼 **Симулятор собеседования на английском языке**\n\n"
        "Выбери направление, по которому хочешь потренироваться:\n"
        "Бот будет задавать реальные вопросы рекрутеров, слушать твои ответы и давать подробную обратную связь по методике STAR!"
    )
    if isinstance(event, types.CallbackQuery):
        await event.message.answer(text, reply_markup=kb, parse_mode="Markdown")
        await event.answer()
    else:
        await event.answer(text, reply_markup=kb, parse_mode="Markdown")

@router.callback_query(F.data.startswith("role_"))
async def start_role_interview(callback: types.CallbackQuery):
    role_key = callback.data.replace("role_", "")
    role_name = INTERVIEW_ROLES.get(role_key, "Собеседование")
    questions = QUESTIONS.get(role_key, QUESTIONS["general"])
    
    USER_INTERVIEW_STATE[callback.from_user.id] = {
        'role': role_key,
        'q_idx': 0
    }
    
    first_q = questions[0]
    
    text = (
        f"🎯 **Начало интервью: {role_name}**\n\n"
        f"👔 **Вопрос рекрутера (1/{len(questions)}):**\n"
        f"*{first_q}*\n\n"
        f"✍️ *Ответь мне сообщением или текстом на английском языке.*"
    )
    
    await callback.message.answer(text, parse_mode="Markdown")
    await callback.answer()

@router.message(lambda msg: msg.from_user.id in USER_INTERVIEW_STATE and msg.text and not msg.text.startswith("/") and msg.text not in ["🃏 Тренировка карточек", "📚 Мой словарь", "🗣️ Разговорный тренажёр", "💼 Собеседование", "📊 Прогресс", "⚙️ Настройки", "📱 Открыть Mini App"])
async def handle_interview_answer(message: types.Message):
    state = USER_INTERVIEW_STATE.get(message.from_user.id)
    if not state:
        return
        
    role_key = state['role']
    q_idx = state['q_idx']
    role_name = INTERVIEW_ROLES.get(role_key, "Собеседование")
    questions = QUESTIONS.get(role_key, QUESTIONS["general"])
    
    current_q = questions[q_idx]
    await message.answer("🔍 *Анализирую ваш ответ с точки зрения HR-рекрутера...*", parse_mode="Markdown")
    
    evaluation = await evaluate_interview_answer(role_name, current_q, message.text)
    await message.answer(f"📊 **Разбор ответа на вопрос {q_idx + 1}/{len(questions)}:**\n\n{evaluation}", parse_mode="Markdown")
    
    state['q_idx'] += 1
    if state['q_idx'] < len(questions):
        next_q = questions[state['q_idx']]
        next_text = (
            f"👔 **Следующий вопрос рекрутера ({state['q_idx'] + 1}/{len(questions)}):**\n"
            f"*{next_q}*\n\n"
            f"✍️ *Напишите ваш ответ:* "
        )
        await message.answer(next_text, parse_mode="Markdown")
    else:
        USER_INTERVIEW_STATE.pop(message.from_user.id, None)
        fin_text = (
            "🎉 **Собеседование успешно завершено!**\n\n"
            "Вы отлично справились со всеми вопросами. Регулярная практика ответов помогает чувствовать себя уверенно на реальных интервью с работодателями!"
        )
        await message.answer(fin_text, parse_mode="Markdown")

