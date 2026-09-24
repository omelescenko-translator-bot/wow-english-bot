# -*- coding: utf-8 -*-
import html
import requests
from datetime import datetime
from aiogram import Router, types, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

import config
from database.db import get_or_create_user, get_stats, SUPPORTED_LANGS

router = Router()

class SupportState(StatesGroup):
    waiting_for_message = State()
    admin_replying = State()

def get_support_keyboard():
    buttons = [
        [
            InlineKeyboardButton(
                text=f"💬 Написать напрямую @{config.DEV_USERNAME}",
                url=f"https://t.me/{config.DEV_USERNAME}"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@router.message(Command("help"))
@router.message(Command("support"))
@router.message(Command("feedback"))
async def cmd_support(message: types.Message, state: FSMContext):
    await state.set_state(SupportState.waiting_for_message)
    text = (
        "💬 <b>Связь с разработчиком & Поддержка</b>\n\n"
        "Напишите ваш вопрос, предложение, идею или сообщение об ошибке <b>прямо сюда в ответном сообщении</b> 👇\n\n"
        "Разработчик сразу же получит ваше обращение и ответит вам прямо в этом чате!\n\n"
        f"<i>Или вы можете написать разработчику напрямую: @{config.DEV_USERNAME}</i>"
    )
    await message.answer(text, reply_markup=get_support_keyboard(), parse_mode="HTML")

@router.callback_query(F.data == "btn_support")
async def cb_support(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SupportState.waiting_for_message)
    await callback.answer()
    text = (
        "💬 <b>Связь с разработчиком & Поддержка</b>\n\n"
        "Напишите ваш вопрос, пожелание или найденную ошибку <b>прямо сюда следующим сообщением</b> 👇\n\n"
        "Разработчик сразу получит ваше сообщение и ответит вам прямо здесь!\n\n"
        f"<i>Прямой контакт: @{config.DEV_USERNAME}</i>"
    )
    await callback.message.answer(text, reply_markup=get_support_keyboard(), parse_mode="HTML")

@router.message(SupportState.waiting_for_message)
async def process_user_support_message(message: types.Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id
    username = message.from_user.username or ""
    full_name = message.from_user.full_name or "Без имени"
    user_text = message.text or message.caption or "(Вложение/медиа)"
    
    # Reset FSM state
    await state.clear()
    
    # Get user language & stats
    user_obj = get_or_create_user(user_id, username, full_name)
    n_code = user_obj.get('native_lang', 'ru')
    t_code = user_obj.get('target_lang', 'en')
    n_meta = SUPPORTED_LANGS.get(n_code, {})
    t_meta = SUPPORTED_LANGS.get(t_code, {})
    lang_pair_str = f"{n_meta.get('flag', '🇷🇺')} ➔ {t_meta.get('flag', '🇬🇧')} {t_meta.get('short', 'EN')}"
    
    now_str = datetime.now().strftime("%d.%m.%Y %H:%M")
    safe_name = html.escape(full_name)
    safe_user = f"@{username}" if username else "—"
    safe_msg = html.escape(user_text)
    
    admin_notification = (
        "🤖 <b>Источник:</b> Бот изучения языков <b>[WOW English AI / @WOWEnglishAI_bot]</b>\n"
        "📩 <b>НОВОЕ СООБЩЕНИЕ ОТ ПОЛЬЗОВАТЕЛЯ (Telegram Bot)</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 <b>От:</b> {safe_name} ({safe_user})\n"
        f"🆔 <b>User ID:</b> <code>{user_id}</code>\n"
        f"🌍 <b>Языки:</b> {lang_pair_str}\n"
        f"⏰ <b>Время:</b> {now_str}\n\n"
        "💬 <b>Текст обращения:</b>\n"
        f"«{safe_msg}»\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        f"✍️ <i>Чтобы ответить, нажмите кнопку ниже или введите:</i>\n"
        f"<code>/reply {user_id} Текст ответа</code>"
    )
    
    admin_buttons = []
    if username:
        admin_buttons.append([InlineKeyboardButton(text=f"💬 Написать @{username}", url=f"https://t.me/{username}")])
    admin_buttons.append([InlineKeyboardButton(text="✍️ Ответить в боте", callback_data=f"adm_reply:{user_id}")])
    admin_kb = InlineKeyboardMarkup(inline_keyboard=admin_buttons)
    
    # Send to main admin and all configured admins
    sent_count = 0
    for admin_id in config.ADMIN_USER_IDS:
        try:
            await bot.send_message(chat_id=admin_id, text=admin_notification, reply_markup=admin_kb, parse_mode="HTML")
            sent_count += 1
        except Exception:
            pass
            
    # Confirm to user
    await message.answer(
        "✅ <b>Ваше сообщение успешно отправлено разработчику!</b>\n\n"
        "Спасибо за обратную связь! Мы внимательно прочитаем ваше сообщение и ответим прямо в этом чате ✨",
        parse_mode="HTML"
    )

# Admin reply via Command: /reply <user_id> <text>
@router.message(Command("reply"))
async def cmd_admin_reply(message: types.Message, bot: Bot):
    admin_id = message.from_user.id
    if not config.is_admin(admin_id):
        return
        
    parts = message.text.split(maxsplit=2)
    if len(parts) < 3:
        await message.answer(
            "⚠️ <b>Формат команды:</b>\n<code>/reply <user_id> <текст ответа></code>\n\n"
            "<i>Пример:</i> <code>/reply 123456789 Спасибо за отзыв, исправили!</code>",
            parse_mode="HTML"
        )
        return
        
    try:
        target_user_id = int(parts[1])
        reply_text = parts[2].strip()
    except ValueError:
        await message.answer("⚠️ Неверный ID пользователя. Укажите числовой ID.")
        return
        
    try:
        user_msg = (
            "💌 <b>Ответ от разработчика:</b>\n\n"
            f"{html.escape(reply_text)}\n\n"
            "<i>Если у вас есть ещё вопросы, просто напишите их в этот чат или вызовите /support ✨</i>"
        )
        await bot.send_message(chat_id=target_user_id, text=user_msg, parse_mode="HTML")
        await message.answer(f"✅ Ответ успешно доставлен пользователю <code>{target_user_id}</code>!", parse_mode="HTML")
    except Exception as e:
        await message.answer(f"❌ Не удалось доставить сообщение пользователю <code>{target_user_id}</code>: {e}", parse_mode="HTML")

# Admin reply via Inline Button
@router.callback_query(F.data.startswith("adm_reply:"))
async def cb_admin_reply_prompt(callback: CallbackQuery, state: FSMContext):
    admin_id = callback.from_user.id
    if not config.is_admin(admin_id):
        await callback.answer("🔒 Доступ запрещен.", show_alert=True)
        return
        
    target_user_id = int(callback.data.split(":")[1])
    await state.set_state(SupportState.admin_replying)
    await state.update_data(target_user_id=target_user_id)
    await callback.answer()
    
    await callback.message.answer(
        f"✍️ <b>Введите текст ответа для пользователя <code>{target_user_id}</code>:</b>\n\n"
        f"<i>(Просто отправьте текст следующим сообщением или нажмите /cancel для отмены)</i>",
        parse_mode="HTML"
    )

@router.message(SupportState.admin_replying)
async def process_admin_reply_text(message: types.Message, state: FSMContext, bot: Bot):
    admin_id = message.from_user.id
    if not config.is_admin(admin_id):
        await state.clear()
        return
        
    if message.text and message.text.startswith("/cancel"):
        await state.clear()
        await message.answer("🚫 Отправка ответа отменена.")
        return
        
    data = await state.get_data()
    target_user_id = data.get('target_user_id')
    reply_text = message.text or message.caption or ""
    await state.clear()
    
    if not target_user_id or not reply_text:
        await message.answer("⚠️ Ошибка: пустой текст или ID пользователя.")
        return
        
    try:
        user_msg = (
            "💌 <b>Ответ от разработчика:</b>\n\n"
            f"{html.escape(reply_text)}\n\n"
            "<i>Если у вас есть ещё вопросы, просто напишите их в этот чат или вызовите /support ✨</i>"
        )
        await bot.send_message(chat_id=target_user_id, text=user_msg, parse_mode="HTML")
        await message.answer(f"✅ Ответ успешно отправлен пользователю <code>{target_user_id}</code>!", parse_mode="HTML")
    except Exception as e:
        await message.answer(f"❌ Не удалось отправить ответ пользователю: {e}")
