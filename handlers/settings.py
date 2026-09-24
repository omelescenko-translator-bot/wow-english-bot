# -*- coding: utf-8 -*-
from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db import get_stats, toggle_ai_mode

router = Router()

@router.message(F.text == "⚙️ Настройки")
async def settings_menu(message: types.Message):
    user_id = message.from_user.id
    stats = get_stats(user_id)
    ai_status = "🟢 Включён" if stats['ai_mode'] else "⚪ Выключен (Чистый словарь 1-в-1)"
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f"AI-обогащение примерами: {'ВЫКЛ ❌' if stats['ai_mode'] else 'ВКЛ 💡'}",
                callback_data="toggle_ai"
            )
        ]
    ])
    
    text = (
        f"⚙️ **Настройки бота:**\n\n"
        f"• **Режим добавления карточек:** {ai_status}\n\n"
        f"💡 *В режиме «Чистый словарь» (по умолчанию) бот сохраняет ровно твои фразы и твой перевод 1-в-1 без лишней воды и выдуманных примеров.*"
    )
    
    await message.answer(text, reply_markup=kb, parse_mode="Markdown")

@router.callback_query(F.data == "toggle_ai")
async def toggle_ai_callback(callback: types.CallbackQuery):
    new_val = toggle_ai_mode(callback.from_user.id)
    ai_status = "🟢 Включён" if new_val else "⚪ Выключен (Чистый словарь 1-в-1)"
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f"AI-обогащение примерами: {'ВЫКЛ ❌' if new_val else 'ВКЛ 💡'}",
                callback_data="toggle_ai"
            )
        ]
    ])
    
    text = (
        f"⚙️ **Настройки бота:**\n\n"
        f"• **Режим добавления карточек:** {ai_status}\n\n"
        f"💡 *В режиме «Чистый словарь» (по умолчанию) бот сохраняет ровно твои фразы и твой перевод 1-в-1 без лишней воды и выдуманных примеров.*"
    )
    
    await callback.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")
    await callback.answer("Настройка обновлена")
