# -*- coding: utf-8 -*-
from aiogram import Router, types, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton, WebAppInfo,
    InlineKeyboardMarkup, InlineKeyboardButton, MenuButtonWebApp
)
from database.db import get_or_create_user, get_stats, get_all_cards, SUPPORTED_LANGS
import config

router = Router()

def get_main_keyboard(user_id: int = None):
    webapp_url = config.get_webapp_url()
    if webapp_url and webapp_url.startswith("https://"):
        target_url = f"{webapp_url}?v=17.0&uid={user_id}" if user_id else f"{webapp_url}?v=17.0"
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(
                        text="📱 Mini App",
                        web_app=WebAppInfo(url=target_url)
                    )
                ]
            ],
            resize_keyboard=True
        )
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Mini App")]],
        resize_keyboard=True
    )

@router.message(CommandStart())
async def cmd_start(message: types.Message, bot: Bot):
    user_id = message.from_user.id
    username = message.from_user.username or ""
    full_name = message.from_user.full_name or ""
    
    # Handle deep link /start reload
    args = message.text.split()[1:] if message.text else []
    if args and args[0].lower() in ['reload', 'update']:
        user_obj = get_or_create_user(user_id, username, full_name)
        stats = get_stats(user_id)
        webapp_url = config.get_webapp_url()
        import time
        target_webapp_url = f"{webapp_url}?v={int(time.time())}&uid={user_id}" if (webapp_url and webapp_url.startswith("https://")) else webapp_url
        if target_webapp_url and target_webapp_url.startswith("https://"):
            try:
                await bot.set_chat_menu_button(
                    chat_id=message.chat.id,
                    menu_button=MenuButtonWebApp(text="Mini App", web_app=WebAppInfo(url=target_webapp_url))
                )
            except Exception:
                pass
        btns = []
        if target_webapp_url and target_webapp_url.startswith("https://"):
            btns.append([InlineKeyboardButton(text="✨ 📱 Открыть обновлённый Mini App ✨", web_app=WebAppInfo(url=target_webapp_url))])
        btns.append([InlineKeyboardButton(text="🃏 Тренировка карточек в чате", callback_data="start_train_cb")])
        await message.answer(
            f"🔄 <b>Бот и Mini App успешно обновлены!</b>\n\n"
            f"📊 <b>В вашем словаре:</b> <code>{stats['total']}</code> карточек\n"
            f"⏳ <b>Учу:</b> <code>{stats['learning']}</code> | ✅ <b>Знаю:</b> <code>{stats['known']}</code>\n\n"
            f"👇 <i>Нажмите кнопку ниже, чтобы открыть обновлённый тренажёр и словарь:</i>",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=btns),
            parse_mode="HTML"
        )
        return

    user_obj = get_or_create_user(user_id, username, full_name)
    n_code = user_obj.get('native_lang', 'ru')
    t_code = user_obj.get('target_lang', 'en')
    n_meta = config.SUPPORTED_LANGS.get(n_code, {})
    t_meta = config.SUPPORTED_LANGS.get(t_code, {})
    
    webapp_url = config.get_webapp_url()
    target_webapp_url = f"{webapp_url}?v=17.0&uid={user_id}" if (webapp_url and webapp_url.startswith("https://")) else webapp_url
    
    # Configure native bottom-left menu button in Telegram specifically for this user
    if target_webapp_url and target_webapp_url.startswith("https://"):
        try:
            await bot.set_chat_menu_button(
                chat_id=message.chat.id,
                menu_button=MenuButtonWebApp(
                    text="Mini App",
                    web_app=WebAppInfo(url=target_webapp_url)
                )
            )
        except Exception as e:
            print("Error setting chat menu button:", e)
    
    stats = get_stats(user_id)
    
    # Inline buttons: Mini App, Open in Browser, Share with Friend
    share_url = "https://t.me/share/url?url=https://t.me/WOWEnglishAI_bot&text=Привет!%20Попробуй%20этот%20интерактивный%20тренажёр%20языков%20в%20Telegram%20Mini%20App!%20🃏✨"
    
    buttons = []
    if target_webapp_url and target_webapp_url.startswith("https://"):
        buttons.append([
            InlineKeyboardButton(
                text="✨ 📱 Открыть Mini App ✨",
                web_app=WebAppInfo(url=target_webapp_url)
            )
        ])
        
    buttons.append([
        InlineKeyboardButton(
            text="🃏 Тренировка карточек в чате",
            callback_data="start_train_cb"
        )
    ])
    
    buttons.append([
        InlineKeyboardButton(
            text="🗣️ Разговорный тренажёр",
            callback_data="start_speaking_cb"
        ),
        InlineKeyboardButton(
            text="💼 Собеседование",
            callback_data="start_interview_cb"
        )
    ])

    buttons.append([
        InlineKeyboardButton(
            text="💌 Поделиться с другом",
            url=share_url
        ),
        InlineKeyboardButton(
            text="💬 Связь с поддержкой",
            callback_data="btn_support"
        )
    ])
    
    inline_kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    import html
    safe_name = html.escape(full_name or 'друг')
    t_name = t_meta.get('name', 'Изучаемый язык')
    lang_flag = f"{n_meta.get('flag', '🇷🇺')} ➔ {t_meta.get('flag', '🇬🇧')} ({t_name})"

    if stats['total'] > 0:
        count_str = f"📊 <b>В вашем словаре:</b> <code>{stats['total']}</code> карточек\n🔥 <b>Серия занятий:</b> <code>{stats['streak']}</code> дн. подряд"
    else:
        count_str = "🌱 <b>Ваш словарь пока чист.</b>\nДобавляйте новые слова через Mini App или отправляйте фразы прямо сюда в чат!"

    text = (
        f"👋 <b>Привет, {safe_name}!</b>\n\n"
        f"Добро пожаловать в персональный интерактивный тренажёр языков!\n"
        f"🌍 <b>Текущая языковая пара:</b> {lang_flag}\n\n"
        f"✨ <b>Возможности и управление:</b>\n"
        f"• 🃏 <b>Интерактивные карточки:</b>\n"
        f"  👈 <i>Свайп влево</i> — <b>«Знаю»</b> (освоено)\n"
        f"  👉 <i>Свайп вправо</i> — <b>«Учу»</b> (повторить)\n"
        f"  ⬇️ <i>Свайп вниз / Корзина</i> — <b>«Удалить»</b>\n"
        f"  🔄 <i>Тап по карточке</i> — 3D-переворот с переводом\n"
        f"• 🔊 <b>Озвучка:</b> чистое произношение на 8 языках\n"
        f"• 🏷 <b>Категории:</b> удобный выбор и создание своих тем\n"
        f"• ➕ <b>AI-добавление:</b> автоперевод в реальном времени\n\n"
        f"{count_str}\n\n"
        f"👇 <b>Нажмите кнопку ниже, чтобы начать:</b>"
    )
    
    await message.answer(text, reply_markup=inline_kb, parse_mode="HTML")


@router.callback_query(F.data.in_(["reload_bot", "reload_app"]))
async def handle_reload_bot_callback(callback: types.CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    username = callback.from_user.username or ""
    full_name = callback.from_user.full_name or ""
    
    get_or_create_user(user_id, username, full_name)
    import time
    webapp_url = config.get_webapp_url()
    target_webapp_url = f"{webapp_url}?v={int(time.time())}&uid={user_id}" if (webapp_url and webapp_url.startswith("https://")) else webapp_url
    
    if target_webapp_url and target_webapp_url.startswith("https://"):
        try:
            await bot.set_chat_menu_button(
                chat_id=callback.message.chat.id,
                menu_button=MenuButtonWebApp(
                    text="Mini App",
                    web_app=WebAppInfo(url=target_webapp_url)
                )
            )
        except Exception:
            pass
            
    stats = get_stats(user_id)
    
    buttons = []
    if target_webapp_url and target_webapp_url.startswith("https://"):
        buttons.append([
            InlineKeyboardButton(
                text="✨ 📱 Открыть обновлённый Mini App ✨",
                web_app=WebAppInfo(url=target_webapp_url)
            )
        ])
    buttons.append([
        InlineKeyboardButton(
            text="🃏 Тренировка карточек в чате",
            callback_data="start_train_cb"
        )
    ])
    
    await callback.answer("✅ Бот и Mini App успешно обновлены!", show_alert=False)
    await callback.message.answer(
        f"🔄 <b>Бот и Mini App успешно обновлены!</b>\n\n"
        f"📊 <b>В вашем словаре:</b> <code>{stats['total']}</code> карточек\n"
        f"⏳ <b>Учу:</b> <code>{stats['learning']}</code> | ✅ <b>Знаю:</b> <code>{stats['known']}</code>\n\n"
        f"👇 <i>Нажмите кнопку ниже, чтобы открыть обновлённый тренажёр и словарь:</i>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
        parse_mode="HTML"
    )

@router.message(F.text == "📊 Прогресс")
async def show_progress(message: types.Message):
    user_id = message.from_user.id
    stats = get_stats(user_id)
    
    text = (
        f"📊 <b>Твоя персональная статистика:</b>\n\n"
        f"🔥 <b>Серия дней подряд:</b> <code>{stats['streak']}</code>\n"
        f"📚 <b>Всего карточек в словаре:</b> <code>{stats['total']}</code>\n"
        f"✅ <b>Освоено (Знаю):</b> <code>{stats['known']}</code>\n"
        f"⏳ <b>В процессе (Учу):</b> <code>{stats['learning']}</code>\n"
        f"🎓 <b>Текущий уровень:</b> <code>{stats['level']}</code>\n\n"
        f"💡 <i>Совет: занимайся каждый день по 5 минут, чтобы слова переходили в долговременную память!</i>"
    )
    await message.answer(text, reply_markup=get_main_keyboard(user_id), parse_mode="HTML")
