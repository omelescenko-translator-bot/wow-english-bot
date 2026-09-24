# -*- coding: utf-8 -*-
import os
import html
from aiogram import Router, types, F, Bot
from aiogram.filters import Command
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile, CallbackQuery, WebAppInfo
)
from database.db import get_admin_analytics, generate_analytics_excel_file
import config

router = Router()

def format_admin_message(data: dict) -> str:
    today_users = data['new_users_today']
    active_today = data['active_today']
    total_users = data['total_users']
    new_7d = data['new_users_7d']
    active_7d = data['active_7d']
    total_cards = data['total_cards']
    known_cards = data['known_cards']
    learning_cards = data['learning_cards']
    avg_cards = data['avg_cards_per_user']
    
    # Top users preview (up to 5)
    top_users_lines = []
    for idx, u in enumerate(data['users_list'][:6], 1):
        u_name = f"@{u['username']}" if u['username'] else html.escape(u['full_name'])
        streak_badge = f"🔥 {u['streak_days']}д" if u['streak_days'] > 1 else "🌱 1д"
        top_users_lines.append(
            f"{idx}. <b>{u_name}</b> — {streak_badge} | 📚 <code>{u['total_cards']}</code> сл. "
            f"(✅<code>{u['known_cards']}</code> / ⏳<code>{u['learning_cards']}</code>)"
        )
        
    users_block = "\n".join(top_users_lines) if top_users_lines else "<i>Пока нет активных учеников</i>"
    
    text = (
        f"👑 <b>ПАНЕЛЬ УПРАВЛЕНИЯ & АНАЛИТИКА WOW ENGLISH</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"👥 <b>Аудитория:</b>\n"
        f"• Всего учеников: <code>{total_users}</code> чел.\n"
        f"• Новых за сегодня: <code>+{today_users}</code> чел.\n"
        f"• Прирост за 7 дней: <code>+{new_7d}</code> чел.\n\n"
        f"⚡ <b>Активность и возвращаемость:</b>\n"
        f"• Активны сегодня (DAU): <code>{active_today}</code> чел.\n"
        f"• Активны за неделю (WAU): <code>{active_7d}</code> чел.\n\n"
        f"📚 <b>Прогресс обучения:</b>\n"
        f"• Всего карточек в базе: <code>{total_cards}</code>\n"
        f"• В среднем на ученика: <code>{avg_cards}</code> сл.\n"
        f"• Выучено (Знаю): <code>{known_cards}</code> шт.\n"
        f"• В процессе (Учу): <code>{learning_cards}</code> шт.\n\n"
        f"🏆 <b>Последние пользователи:</b>\n"
        f"{users_block}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"💡 <i>Нажмите «📥 Скачать Excel», чтобы получить полную детальную выгрузку по каждому человеку.</i>"
    )
    return text

def get_admin_keyboard(user_id: int):
    webapp_url = config.get_webapp_url()
    admin_webapp_url = f"{webapp_url}?uid={user_id}&tab=analytics" if webapp_url else None
    
    buttons = [
        [
            InlineKeyboardButton(text="🔄 Обновить сводку", callback_data="admin_refresh"),
            InlineKeyboardButton(text="📥 Скачать Excel", callback_data="admin_download_excel")
        ]
    ]
    
    if admin_webapp_url and admin_webapp_url.startswith("https://"):
        buttons.insert(0, [
            InlineKeyboardButton(
                text="📊 Открыть дашборд в Mini App",
                web_app=WebAppInfo(url=admin_webapp_url)
            )
        ])
        
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@router.message(Command("admin"))
@router.message(Command("stats"))
async def cmd_admin(message: types.Message):
    user_id = message.from_user.id
    if not config.is_admin(user_id):
        await message.answer("🔒 Данный раздел доступен только администратору бота.")
        return
        
    data = get_admin_analytics()
    text = format_admin_message(data)
    await message.answer(text, reply_markup=get_admin_keyboard(user_id), parse_mode="HTML")

@router.callback_query(F.data == "admin_refresh")
async def cb_admin_refresh(callback: CallbackQuery):
    user_id = callback.from_user.id
    if not config.is_admin(user_id):
        await callback.answer("🔒 Доступ запрещен.", show_alert=True)
        return
        
    data = get_admin_analytics()
    text = format_admin_message(data)
    try:
        await callback.message.edit_text(text, reply_markup=get_admin_keyboard(user_id), parse_mode="HTML")
        await callback.answer("✅ Данные обновлены!")
    except Exception:
        await callback.answer("✅ Данные актуальны.")

@router.callback_query(F.data == "admin_download_excel")
async def cb_admin_download_excel(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    if not config.is_admin(user_id):
        await callback.answer("🔒 Доступ запрещен.", show_alert=True)
        return
        
    await callback.answer("⏳ Формирую Excel отчёт...")
    excel_path = generate_analytics_excel_file()
    
    if os.path.exists(excel_path):
        file = FSInputFile(excel_path, filename="WOW_English_Analytics.xlsx")
        await bot.send_document(
            chat_id=callback.message.chat.id,
            document=file,
            caption="📊 <b>Полная выгрузка метрик и пользователей WOW English</b>\nВключает сводку, историю активности и прогресс по каждому ученику.",
            parse_mode="HTML"
        )
    else:
        await callback.message.answer("⚠️ Ошибка при создании файла отчёта.")
