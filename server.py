# -*- coding: utf-8 -*-
import os
import sys

try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional

from database.db import (
    get_all_cards, add_card, update_card_review, set_card_status, get_stats, get_or_create_user,
    import_cards_bulk, delete_card, update_card_category, get_admin_analytics, generate_analytics_excel_file,
    set_user_languages, get_user_categories, SUPPORTED_LANGS,
    ensure_user_groups, get_user_groups, update_group_name, update_group_status, reset_group_result,
    update_card_trainer_status, get_red_cards
)
from seed_initial_data import categorize
from translator import smart_translate
from news_service import generate_news_context_stories
import config

app = FastAPI(title="English Learning WebApp Backend")

WEBAPP_DIR = os.path.join(os.path.dirname(__file__), 'webapp')

class NewsContextRequest(BaseModel):
    user_id: int
    words: List[dict]
    target_lang: Optional[str] = "en"
    native_lang: Optional[str] = "ru"

class TranslateRequest(BaseModel):
    text: str
    source_field: Optional[str] = "auto" # 'target', 'native', 'auto'
    native_lang: Optional[str] = "ru"
    target_lang: Optional[str] = "en"

class CardCreate(BaseModel):
    user_id: int
    phrase_en: str # Target phrase
    phrase_ru: str = "" # Native translation
    category: str = "Общее"
    target_lang: Optional[str] = "en"
    native_lang: Optional[str] = "ru"

class CardDeleteRequest(BaseModel):
    card_id: int
    user_id: int

class BulkImportRequest(BaseModel):
    user_id: int
    raw_text: str
    target_lang: Optional[str] = "en"
    native_lang: Optional[str] = "ru"

class SupportFeedbackRequest(BaseModel):
    user_id: int
    message: str
    category: Optional[str] = "Обратная связь"
    native_lang: Optional[str] = "ru"
    target_lang: Optional[str] = "en"

class CardBulkImport(BaseModel):
    user_id: int
    raw_text: Optional[str] = ""
    cards: Optional[List[dict]] = None
    target_lang: Optional[str] = "en"
    native_lang: Optional[str] = "ru"

class UserLanguagesUpdate(BaseModel):
    user_id: int
    native_lang: str
    target_lang: str

class CardStatusUpdate(BaseModel):
    card_id: int
    status: str # 'learning' or 'known'
    user_id: Optional[int] = None

class CardReview(BaseModel):
    card_id: int
    quality: int
    user_id: Optional[int] = None

class GroupNameUpdate(BaseModel):
    group_id: int
    name: str
    user_id: int

class GroupStatusUpdate(BaseModel):
    group_id: int
    status: str # 'new', 'in_progress', 'mastered'
    user_id: int

class GroupResetRequest(BaseModel):
    group_id: int
    user_id: int

class CardTrainerStatusUpdate(BaseModel):
    card_id: int
    trainer_status: str # 'green', 'red', 'neutral'
    user_id: int

@app.get("/api/cards")
def get_cards_endpoint(user_id: Optional[int] = None, status: str = 'all', shuffle: bool = True, target_lang: Optional[str] = None, native_lang: Optional[str] = None):
    if user_id is None:
        return []
    get_or_create_user(user_id)
    status_filter = None if status == 'all' else status
    cards = get_all_cards(user_id, status_filter=status_filter, shuffle=shuffle, target_lang=target_lang, native_lang=native_lang)
    return cards

@app.post("/api/card_status")
def set_status_endpoint(req: CardStatusUpdate):
    res = set_card_status(req.card_id, req.status, user_id=req.user_id)
    return {"status": "ok", "result": res}

import asyncio

@app.post("/api/translate")
async def translate_endpoint(req: TranslateRequest):
    if not req.text or not req.text.strip():
        raise HTTPException(status_code=400, detail="Text is required")
    res = await asyncio.to_thread(
        smart_translate, 
        req.text, 
        req.source_field, 
        native_lang=req.native_lang or "ru", 
        target_lang=req.target_lang or "en"
    )
    return res

@app.post("/api/cards")
def create_card_endpoint(card: CardCreate):
    card_id = add_card(
        card.user_id, 
        card.phrase_en, 
        card.phrase_ru, 
        card.category, 
        status="learning",
        target_lang=card.target_lang or "en",
        native_lang=card.native_lang or "ru"
    )
    if not card_id:
        raise HTTPException(status_code=400, detail="Invalid card data")
    return {"status": "ok", "card_id": card_id}

@app.post("/api/user/languages")
def update_user_languages_endpoint(req: UserLanguagesUpdate):
    get_or_create_user(req.user_id)
    res = set_user_languages(req.user_id, req.native_lang, req.target_lang)
    return {"status": "ok", "languages": res}

@app.delete("/api/cards/{card_id}")
def delete_card_endpoint(card_id: int, user_id: int = Query(..., description="Telegram User ID")):
    deleted = delete_card(card_id, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Card not found or unauthorized")
    return {"status": "ok", "deleted": True}

def parse_text_lines_smart(raw_text: str):
    lines = raw_text.strip().split('\n')
    parsed_cards = []
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
            
        en, ru = '', ''
        # Excel Tab separator
        if '\t' in line:
            parts = line.split('\t')
            en = parts[0].strip()
            ru = parts[1].strip() if len(parts) > 1 else ''
        elif ' — ' in line:
            parts = line.split(' — ', 1)
            en, ru = parts[0].strip(), parts[1].strip()
        elif ' - ' in line:
            parts = line.split(' - ', 1)
            en, ru = parts[0].strip(), parts[1].strip()
        elif ':' in line:
            parts = line.split(':', 1)
            en, ru = parts[0].strip(), parts[1].strip()
        else:
            en = line
            ru = ''
            
        # Skip header lines from Excel
        if en.lower() in ['предложение', 'phrase', 'english', 'слово'] and ru.lower() in ['перевод', 'translation', 'russian']:
            continue
            
        # Auto-detect language if columns were reversed (e.g. RU in col 1, EN in col 2)
        has_ru_in_en = any(c in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя' for c in en.lower())
        has_en_in_ru = any(c in 'abcdefghijklmnopqrstuvwxyz' for c in ru.lower())
        if has_ru_in_en and has_en_in_ru and not any(c in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя' for c in ru.lower()):
            en, ru = ru, en
            
        if en or ru:
            cat = categorize(en, ru)
            parsed_cards.append((en, ru, cat))
            
    return parsed_cards

@app.post("/api/cards/bulk")
def bulk_import_endpoint(req: CardBulkImport):
    get_or_create_user(req.user_id)
    cards_to_add = []
    
    if req.cards:
        for c in req.cards:
            en = c.get('phrase_en', '').strip()
            ru = c.get('phrase_ru', '').strip()
            cat = c.get('category', categorize(en, ru))
            if en or ru:
                cards_to_add.append((en, ru, cat))
    elif req.raw_text:
        cards_to_add = parse_text_lines_smart(req.raw_text)
        
    if not cards_to_add:
        raise HTTPException(status_code=400, detail="Не удалось распознать фразы для импорта")
        
    added = import_cards_bulk(
        req.user_id, 
        cards_to_add, 
        target_lang=req.target_lang or "en", 
        native_lang=req.native_lang or "ru"
    )
    return {"status": "ok", "added_count": added, "total_received": len(cards_to_add)}

@app.post("/api/review")
def review_card_endpoint(review: CardReview):
    res = update_card_review(review.card_id, review.quality, user_id=review.user_id)
    return {"status": "ok", "result": res}

class CardCategoryUpdate(BaseModel):
    card_id: int
    category: str
    user_id: Optional[int] = None

@app.post("/api/card/category")
def update_category_endpoint(req: CardCategoryUpdate):
    success = update_card_category(req.card_id, req.category, user_id=req.user_id)
    return {"status": "ok" if success else "not_found", "updated": success, "category": req.category}

@app.post("/api/card/delete")
def delete_card_endpoint(req: CardDeleteRequest):
    success = delete_card(req.card_id, user_id=req.user_id)
    return {"status": "ok" if success else "not_found", "deleted": success}

@app.get("/api/categories")
def get_categories_endpoint(user_id: int, target_lang: Optional[str] = "en", native_lang: Optional[str] = "ru"):
    return get_user_categories(user_id, target_lang=target_lang, native_lang=native_lang)

@app.get("/api/groups")
def get_groups_endpoint(user_id: int, target_lang: Optional[str] = "en", native_lang: Optional[str] = "ru"):
    get_or_create_user(user_id)
    return ensure_user_groups(user_id, target_lang=target_lang, native_lang=native_lang)

@app.post("/api/group/name")
def update_group_name_endpoint(req: GroupNameUpdate):
    success = update_group_name(req.group_id, req.name, user_id=req.user_id)
    return {"status": "ok" if success else "error", "updated": success}

@app.post("/api/group/status")
def update_group_status_endpoint(req: GroupStatusUpdate):
    success = update_group_status(req.group_id, req.status, user_id=req.user_id)
    return {"status": "ok" if success else "error", "updated": success}

@app.post("/api/group/reset")
def reset_group_endpoint(req: GroupResetRequest):
    success = reset_group_result(req.group_id, user_id=req.user_id)
    return {"status": "ok" if success else "error", "reset": success}

@app.post("/api/card/trainer_status")
def update_trainer_status_endpoint(req: CardTrainerStatusUpdate):
    res = update_card_trainer_status(req.card_id, req.trainer_status, user_id=req.user_id)
    if not res:
        raise HTTPException(status_code=400, detail="Invalid trainer status")
    return res

@app.get("/api/cards/red")
def get_red_cards_endpoint(user_id: int, target_lang: Optional[str] = "en", native_lang: Optional[str] = "ru"):
    get_or_create_user(user_id)
    return get_red_cards(user_id, target_lang=target_lang, native_lang=native_lang)

@app.post("/api/trainer/news_context")
async def get_trainer_news_context(req: NewsContextRequest):
    get_or_create_user(req.user_id)
    stories = await asyncio.to_thread(
        generate_news_context_stories,
        req.words,
        target_lang=req.target_lang or "en",
        native_lang=req.native_lang or "ru"
    )
    return {"status": "ok", "stories": stories}

@app.get("/api/stats")
def stats_endpoint(user_id: Optional[int] = None, target_lang: Optional[str] = None, native_lang: Optional[str] = None):
    if user_id is None:
        return {'total': 0, 'learning': 0, 'known': 0, 'streak': 1, 'level': 'B1 Intermediate', 'ai_mode': False, 'native_lang': 'ru', 'target_lang': 'en'}
    return get_stats(user_id, target_lang=target_lang, native_lang=native_lang)

@app.get("/api/admin/analytics")
def get_admin_analytics_endpoint(user_id: Optional[int] = None):
    if not config.is_admin(user_id):
        raise HTTPException(status_code=403, detail="Доступ запрещен. Только для администратора.")
    return get_admin_analytics()

@app.get("/api/admin/export-excel")
def export_admin_excel_endpoint(user_id: Optional[int] = None):
    if not config.is_admin(user_id):
        raise HTTPException(status_code=403, detail="Доступ запрещен. Только для администратора.")
    excel_path = generate_analytics_excel_file()
    return FileResponse(
        excel_path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename="WOW_Languages_Analytics.xlsx"
    )

@app.post("/api/support")
def send_support_message_endpoint(req: SupportFeedbackRequest):
    if not req.message or not req.message.strip():
        raise HTTPException(status_code=400, detail="Текст сообщения не может быть пустым")
        
    user = get_or_create_user(req.user_id)
    username = user.get('username', '')
    full_name = user.get('full_name', 'Ученик')
    
    n_code = req.native_lang or user.get('native_lang', 'ru')
    t_code = req.target_lang or user.get('target_lang', 'en')
    n_meta = SUPPORTED_LANGS.get(n_code, {})
    t_meta = SUPPORTED_LANGS.get(t_code, {})
    lang_str = f"{n_meta.get('flag', '🇷🇺')} ➔ {t_meta.get('flag', '🇬🇧')} {t_meta.get('short', 'EN')}"
    
    import html, datetime, requests
    now_str = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    safe_name = html.escape(full_name)
    safe_user = f"@{username}" if username else "—"
    safe_cat = html.escape(req.category or "Обратная связь")
    safe_msg = html.escape(req.message.strip())
    
    notification_text = (
        f"🤖 <b>Источник:</b> Бот изучения языков <b>[WOW English AI / @WOWEnglishAI_bot]</b>\n"
        f"📩 <b>НОВОЕ ОБРАЩЕНИЕ (Mini App)</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 <b>От:</b> {safe_name} ({safe_user})\n"
        f"🆔 <b>User ID:</b> <code>{req.user_id}</code>\n"
        f"🏷 <b>Категория:</b> {safe_cat}\n"
        f"🌍 <b>Языки:</b> {lang_str}\n"
        f"⏰ <b>Время:</b> {now_str}\n\n"
        f"💬 <b>Текст сообщения:</b>\n"
        f"«{safe_msg}»\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"✍️ <i>Чтобы ответить, введите:</i>\n"
        f"<code>/reply {req.user_id} Текст ответа</code>"
    )
    
    bot_token = config.BOT_TOKEN
    sent_count = 0
    if bot_token:
        for admin_id in config.ADMIN_USER_IDS:
            try:
                inline_kb = {
                    "inline_keyboard": [
                        [{"text": f"💬 Написать @{username}", "url": f"https://t.me/{username}"}] if username else [],
                        [{"text": "✍️ Ответить в боте", "callback_data": f"adm_reply:{req.user_id}"}]
                    ]
                }
                inline_kb["inline_keyboard"] = [r for r in inline_kb["inline_keyboard"] if r]
                
                res = requests.post(
                    f"https://api.telegram.org/bot{bot_token}/sendMessage",
                    json={
                        "chat_id": admin_id,
                        "text": notification_text,
                        "parse_mode": "HTML",
                        "reply_markup": inline_kb
                    },
                    timeout=5
                )
                if res.status_code == 200:
                    sent_count += 1
            except Exception as e:
                print(f"Error notifying admin {admin_id}: {e}")
                
    return {"status": "ok", "delivered_admins": sent_count}

@app.get("/api/admin/check")
def check_is_admin_endpoint(user_id: Optional[int] = None):
    return {"is_admin": config.is_admin(user_id)}

@app.get("/style.css")
def serve_style_css():
    css_path = os.path.join(WEBAPP_DIR, 'style.css')
    return FileResponse(
        css_path,
        media_type="text/css; charset=utf-8",
        headers={"Cache-Control": "no-cache, no-store, must-revalidate", "Pragma": "no-cache"}
    )

@app.get("/app.js")
def serve_app_js():
    js_path = os.path.join(WEBAPP_DIR, 'app.js')
    return FileResponse(
        js_path,
        media_type="application/javascript; charset=utf-8",
        headers={"Cache-Control": "no-cache, no-store, must-revalidate", "Pragma": "no-cache"}
    )

# Serve WebApp frontend
app.mount("/static", StaticFiles(directory=WEBAPP_DIR), name="static")

@app.api_route("/health", methods=["GET", "HEAD"])
def health_check():
    return {"status": "ok"}

@app.api_route("/", methods=["GET", "HEAD"])
def serve_index():
    return FileResponse(
        os.path.join(WEBAPP_DIR, 'index.html'),
        media_type="text/html; charset=utf-8",
        headers={"Cache-Control": "no-cache, no-store, must-revalidate", "Pragma": "no-cache"}
    )

@app.get("/{file_name}")
def serve_webapp_file(file_name: str):
    fpath = os.path.join(WEBAPP_DIR, file_name)
    if os.path.exists(fpath):
        if file_name.endswith('.css'):
            return FileResponse(fpath, media_type="text/css; charset=utf-8", headers={"Cache-Control": "no-cache"})
        if file_name.endswith('.js'):
            return FileResponse(fpath, media_type="application/javascript; charset=utf-8", headers={"Cache-Control": "no-cache"})
        return FileResponse(fpath)
    return FileResponse(os.path.join(WEBAPP_DIR, 'index.html'))

if __name__ == '__main__':
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    host = "0.0.0.0" if (os.getenv("RENDER") or os.getenv("PORT") or sys.platform != 'win32') else "127.0.0.1"
    uvicorn.run(app, host=host, port=port)
