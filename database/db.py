# -*- coding: utf-8 -*-
import sqlite3
import os
import random
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'vocabulary.db')

SUPPORTED_LANGS = {
    'en': {'name': 'English (Английский)', 'flag': '🇬🇧', 'short': 'EN', 'speech_code': 'en-US'},
    'ru': {'name': 'Русский', 'flag': '🇷🇺', 'short': 'RU', 'speech_code': 'ru-RU'},
    'uk': {'name': 'Українська (Украинский)', 'flag': '🇺🇦', 'short': 'UK', 'speech_code': 'uk-UA'},
    'es': {'name': 'Español (Испанский)', 'flag': '🇪🇸', 'short': 'ES', 'speech_code': 'es-ES'},
    'fr': {'name': 'Français (Французский)', 'flag': '🇫🇷', 'short': 'FR', 'speech_code': 'fr-FR'},
    'de': {'name': 'Deutsch (Немецкий)', 'flag': '🇩🇪', 'short': 'DE', 'speech_code': 'de-DE'},
    'it': {'name': 'Italiano (Итальянский)', 'flag': '🇮🇹', 'short': 'IT', 'speech_code': 'it-IT'},
    'sl': {'name': 'Slovenščina (Словенский)', 'flag': '🇸🇮', 'short': 'SL', 'speech_code': 'sl-SI'}
}

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            full_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            streak_days INTEGER DEFAULT 1,
            last_active_date TEXT,
            level TEXT DEFAULT 'B1 Intermediate',
            ai_enrich_mode INTEGER DEFAULT 0,
            native_lang TEXT DEFAULT 'ru',
            target_lang TEXT DEFAULT 'en'
        )
    ''')
    
    # Flashcards table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            phrase_en TEXT NOT NULL,
            phrase_ru TEXT NOT NULL,
            category TEXT DEFAULT 'Общее',
            status TEXT DEFAULT 'learning',
            repetitions INTEGER DEFAULT 0,
            interval_days INTEGER DEFAULT 1,
            next_review_date TEXT,
            ease_factor REAL DEFAULT 2.5,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            target_lang TEXT DEFAULT 'en',
            native_lang TEXT DEFAULT 'ru',
            group_id INTEGER,
            trainer_status TEXT DEFAULT 'neutral',
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')

    # Study Groups table (for 10-phrase batch progression and trainer)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS study_groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            group_order INTEGER NOT NULL,
            name TEXT NOT NULL,
            status TEXT DEFAULT 'new',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            target_lang TEXT DEFAULT 'en',
            native_lang TEXT DEFAULT 'ru',
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    
    # Migrate users columns
    cursor.execute("PRAGMA table_info(users)")
    u_cols = [row['name'] for row in cursor.fetchall()]
    if 'native_lang' not in u_cols:
        cursor.execute("ALTER TABLE users ADD COLUMN native_lang TEXT DEFAULT 'ru'")
    if 'target_lang' not in u_cols:
        cursor.execute("ALTER TABLE users ADD COLUMN target_lang TEXT DEFAULT 'en'")
    
    # Migrate cards columns
    cursor.execute("PRAGMA table_info(cards)")
    c_cols = [row['name'] for row in cursor.fetchall()]
    if 'status' not in c_cols:
        cursor.execute("ALTER TABLE cards ADD COLUMN status TEXT DEFAULT 'learning'")
    if 'target_lang' not in c_cols:
        cursor.execute("ALTER TABLE cards ADD COLUMN target_lang TEXT DEFAULT 'en'")
    if 'native_lang' not in c_cols:
        cursor.execute("ALTER TABLE cards ADD COLUMN native_lang TEXT DEFAULT 'ru'")
    if 'group_id' not in c_cols:
        cursor.execute("ALTER TABLE cards ADD COLUMN group_id INTEGER")
    if 'trainer_status' not in c_cols:
        cursor.execute("ALTER TABLE cards ADD COLUMN trainer_status TEXT DEFAULT 'neutral'")
        
    conn.commit()
    conn.close()

def get_or_create_user(user_id: int, username: str = '', full_name: str = '', native_lang: str = None, target_lang: str = None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    
    today = datetime.now().strftime('%Y-%m-%d')
    if not user:
        n_lang = native_lang if native_lang in SUPPORTED_LANGS else 'ru'
        t_lang = target_lang if target_lang in SUPPORTED_LANGS else 'en'
        cursor.execute('''
            INSERT INTO users (user_id, username, full_name, streak_days, last_active_date, native_lang, target_lang)
            VALUES (?, ?, ?, 1, ?, ?, ?)
        ''', (user_id, username, full_name, today, n_lang, t_lang))
        conn.commit()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()
    else:
        last_date = user['last_active_date']
        streak = user['streak_days']
        update_fields = []
        params = []
        
        if last_date != today:
            if last_date:
                try:
                    last_dt = datetime.strptime(last_date, '%Y-%m-%d')
                    if (datetime.now() - last_dt).days == 1:
                        streak += 1
                    elif (datetime.now() - last_dt).days > 1:
                        streak = 1
                except Exception:
                    pass
            update_fields.extend(['last_active_date = ?', 'streak_days = ?'])
            params.extend([today, streak])
            
        if username and username != user['username']:
            update_fields.append('username = ?')
            params.append(username)
        if full_name and full_name != user['full_name']:
            update_fields.append('full_name = ?')
            params.append(full_name)
            
        if update_fields:
            params.append(user_id)
            cursor.execute(f'UPDATE users SET {", ".join(update_fields)} WHERE user_id = ?', params)
            conn.commit()
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            user = cursor.fetchone()
            
    conn.close()
    return dict(user)

def set_user_languages(user_id: int, native_lang: str, target_lang: str):
    conn = get_connection()
    cursor = conn.cursor()
    n_lang = native_lang if native_lang in SUPPORTED_LANGS else 'ru'
    t_lang = target_lang if target_lang in SUPPORTED_LANGS else 'en'
    
    cursor.execute('''
        UPDATE users 
        SET native_lang = ?, target_lang = ?
        WHERE user_id = ?
    ''', (n_lang, t_lang, user_id))
    conn.commit()
    conn.close()
    return {'native_lang': n_lang, 'target_lang': t_lang}

def get_all_user_ids():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT user_id FROM users')
    rows = cursor.fetchall()
    conn.close()
    return [r['user_id'] for r in rows if r['user_id']]

def add_card(user_id: int, phrase_en: str, phrase_ru: str, category: str = 'Общее', status: str = 'learning', target_lang: str = 'en', native_lang: str = 'ru'):
    phrase_en = phrase_en.strip()
    phrase_ru = phrase_ru.strip()
    if not phrase_en and not phrase_ru:
        return None
    
    if not phrase_ru and phrase_en:
        phrase_ru = '—'
    if not phrase_en and phrase_ru:
        phrase_en = '—'
        
    t_lang = target_lang if target_lang in SUPPORTED_LANGS else 'en'
    n_lang = native_lang if native_lang in SUPPORTED_LANGS else 'ru'
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id FROM cards 
        WHERE user_id = ? AND LOWER(phrase_en) = LOWER(?) AND (target_lang = ? OR target_lang IS NULL)
    ''', (user_id, phrase_en, t_lang))
    existing = cursor.fetchone()
    
    today = datetime.now().strftime('%Y-%m-%d')
    if existing:
        cursor.execute('''
            UPDATE cards 
            SET phrase_ru = ?, category = ?, target_lang = ?, native_lang = ?
            WHERE id = ? AND user_id = ?
        ''', (phrase_ru, category, t_lang, n_lang, existing['id'], user_id))
        card_id = existing['id']
    else:
        cursor.execute('''
            INSERT INTO cards (user_id, phrase_en, phrase_ru, category, status, target_lang, native_lang, next_review_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, phrase_en, phrase_ru, category, status, t_lang, n_lang, today))
        card_id = cursor.lastrowid
        
    conn.commit()
    conn.close()
    
    # Auto-synchronize groups immediately
    try:
        ensure_user_groups(user_id, target_lang=t_lang, native_lang=n_lang)
    except Exception:
        pass
        
    return card_id

def import_cards_bulk(user_id: int, cards_list: list, target_lang: str = 'en', native_lang: str = 'ru'):
    t_lang = target_lang if target_lang in SUPPORTED_LANGS else 'en'
    n_lang = native_lang if native_lang in SUPPORTED_LANGS else 'ru'
    added = 0
    for item in cards_list:
        if len(item) == 2:
            en, ru = item
            cat = 'Общее'
        else:
            en, ru, cat = item
        if add_card(user_id, en, ru, cat, target_lang=t_lang, native_lang=n_lang):
            added += 1
            
    try:
        ensure_user_groups(user_id, target_lang=t_lang, native_lang=n_lang)
    except Exception:
        pass
        
    return added

def get_all_cards(user_id: int, search_query: str = None, status_filter: str = None, shuffle: bool = False, target_lang: str = None, native_lang: str = None):
    conn = get_connection()
    cursor = conn.cursor()
    query = 'SELECT * FROM cards WHERE user_id = ?'
    params = [user_id]
    
    if target_lang and target_lang in SUPPORTED_LANGS:
        query += ' AND target_lang = ?'
        params.append(target_lang)
    if native_lang and native_lang in SUPPORTED_LANGS:
        query += ' AND native_lang = ?'
        params.append(native_lang)
        
    if status_filter and status_filter in ['learning', 'known']:
        query += ' AND status = ?'
        params.append(status_filter)
        
    if search_query:
        query += ' AND (phrase_en LIKE ? OR phrase_ru LIKE ?)'
        params.extend([f'%{search_query}%', f'%{search_query}%'])
        
    query += ' ORDER BY id DESC'
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    result = [dict(r) for r in rows]
    if shuffle:
        random.shuffle(result)
    return result

def set_card_status(card_id: int, status: str, user_id: int = None):
    """status: 'learning' or 'known'"""
    conn = get_connection()
    cursor = conn.cursor()
    
    today = datetime.now().strftime('%Y-%m-%d')
    if status == 'known':
        repetitions = 3
        interval = 7
        next_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
    else:
        status = 'learning'
        repetitions = 0
        interval = 1
        next_date = today
        
    if user_id is not None:
        cursor.execute('''
            UPDATE cards 
            SET status = ?, repetitions = ?, interval_days = ?, next_review_date = ?
            WHERE id = ? AND user_id = ?
        ''', (status, repetitions, interval, next_date, card_id, user_id))
    else:
        cursor.execute('''
            UPDATE cards 
            SET status = ?, repetitions = ?, interval_days = ?, next_review_date = ?
            WHERE id = ?
        ''', (status, repetitions, interval, next_date, card_id))
        
    conn.commit()
    conn.close()
    return {'card_id': card_id, 'status': status}

def update_card_review(card_id: int, quality: int, user_id: int = None):
    """
    quality: 
    1 = Учу (повторить) -> status = 'learning'
    5 = Знаю -> status = 'known'
    """
    status = 'known' if quality >= 3 else 'learning'
    return set_card_status(card_id, status, user_id=user_id)

def delete_card(card_id: int, user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT target_lang, native_lang FROM cards WHERE id = ? AND user_id = ?', (card_id, user_id))
    row = cursor.fetchone()
    t_lang = row['target_lang'] if row else 'en'
    n_lang = row['native_lang'] if row else 'ru'
    
    cursor.execute('DELETE FROM cards WHERE id = ? AND user_id = ?', (card_id, user_id))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    
    if affected > 0:
        try:
            ensure_user_groups(user_id, target_lang=t_lang, native_lang=n_lang)
        except Exception:
            pass
            
    return affected > 0

def update_card_category(card_id: int, category: str, user_id: int = None) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    clean_cat = category.strip() if category else ""
    if user_id:
        cursor.execute('UPDATE cards SET category = ? WHERE id = ? AND user_id = ?', (clean_cat, card_id, user_id))
    else:
        cursor.execute('UPDATE cards SET category = ? WHERE id = ?', (clean_cat, card_id))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0

def get_user_categories(user_id: int, target_lang: str = None, native_lang: str = "ru"):
    """
    Returns categories for user's vocabulary.
    Rule: If total cards < 30, returns [] (no custom categories, only 'All').
    If total cards >= 30, returns distinct meaningful categories or triggers AI clustering.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    query = 'SELECT * FROM cards WHERE user_id = ?'
    params = [user_id]
    if target_lang and target_lang in SUPPORTED_LANGS:
        query += ' AND target_lang = ?'
        params.append(target_lang)
    if native_lang and native_lang in SUPPORTED_LANGS:
        query += ' AND native_lang = ?'
        params.append(native_lang)
        
    cursor.execute(query, params)
    rows = cursor.fetchall()
    cards = [dict(r) for r in rows]
    total_count = len(cards)
    
    if total_count < 30:
        conn.close()
        return {'total_cards': total_count, 'categories': []}
        
    # Check existing distinct categories (ignore corrupt or placeholder categories)
    existing_cats = [
        c['category'].strip() for c in cards 
        if c.get('category') and c['category'].strip() 
        and c['category'].strip() not in ['Общее', 'General', '—', '']
        and '\ufffd' not in c['category']
    ]
    unique_existing = list(dict.fromkeys(existing_cats))
    
    if len(unique_existing) >= 2:
        conn.close()
        return {'total_cards': total_count, 'categories': unique_existing}
        
    # Trigger AI clustering for >= 30 cards
    try:
        from translator import categorize_user_vocabulary
        categorization_result = categorize_user_vocabulary(cards, native_lang=native_lang, target_lang=target_lang or 'en')
        new_categories = categorization_result.get('categories', [])
        card_map = categorization_result.get('card_categories', {})
        
        if card_map:
            for card_id_str, cat_name in card_map.items():
                try:
                    c_id = int(card_id_str)
                    cursor.execute('UPDATE cards SET category = ? WHERE id = ? AND user_id = ?', (cat_name, c_id, user_id))
                except Exception:
                    pass
            conn.commit()
            
        conn.close()
        return {'total_cards': total_count, 'categories': new_categories}
    except Exception as e:
        conn.close()
        return {'total_cards': total_count, 'categories': []}

def get_stats(user_id: int, target_lang: str = None, native_lang: str = None):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    streak = user['streak_days'] if user else 1
    level = user['level'] if user else 'B1 Intermediate'
    ai_mode = user['ai_enrich_mode'] if user else 0
    u_native_lang = user['native_lang'] if (user and 'native_lang' in user.keys() and user['native_lang']) else 'ru'
    u_target_lang = user['target_lang'] if (user and 'target_lang' in user.keys() and user['target_lang']) else 'en'
    
    t_lang = target_lang or u_target_lang
    n_lang = native_lang or u_native_lang
    
    card_query_base = 'FROM cards WHERE user_id = ?'
    card_params = [user_id]
    if t_lang:
        card_query_base += ' AND target_lang = ?'
        card_params.append(t_lang)
    if n_lang:
        card_query_base += ' AND native_lang = ?'
        card_params.append(n_lang)
        
    cursor.execute(f'SELECT COUNT(*) as total {card_query_base}', card_params)
    total_row = cursor.fetchone()
    total = total_row['total'] if total_row else 0
    
    cursor.execute(f"SELECT COUNT(*) as known {card_query_base} AND status = 'known'", card_params)
    known_row = cursor.fetchone()
    known = known_row['known'] if known_row else 0
    
    cursor.execute(f"SELECT COUNT(*) as learning {card_query_base} AND (status = 'learning' OR status IS NULL)", card_params)
    learning_row = cursor.fetchone()
    learning = learning_row['learning'] if learning_row else 0
    
    conn.close()
    return {
        'total': total,
        'learning': learning,
        'known': known,
        'streak': streak,
        'level': level,
        'ai_mode': bool(ai_mode),
        'native_lang': n_lang,
        'target_lang': t_lang,
        'supported_langs': SUPPORTED_LANGS
    }

def toggle_ai_mode(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT ai_enrich_mode FROM users WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    new_val = 1 if (not row or row['ai_enrich_mode'] == 0) else 0
    cursor.execute('UPDATE users SET ai_enrich_mode = ? WHERE user_id = ?', (new_val, user_id))
    conn.commit()
    conn.close()
    return bool(new_val)

def get_admin_analytics():
    conn = get_connection()
    cursor = conn.cursor()
    
    today = datetime.now().strftime('%Y-%m-%d')
    week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    # 1. Total users
    cursor.execute('SELECT COUNT(*) as total FROM users')
    total_users = cursor.fetchone()['total'] or 0
    
    # 2. New users today & last 7d
    cursor.execute('SELECT COUNT(*) as cnt FROM users WHERE DATE(created_at) = ?', (today,))
    new_users_today = cursor.fetchone()['cnt'] or 0
    
    cursor.execute('SELECT COUNT(*) as cnt FROM users WHERE DATE(created_at) >= ?', (week_ago,))
    new_users_7d = cursor.fetchone()['cnt'] or 0
    
    # 3. Active users today & last 7d
    cursor.execute('SELECT COUNT(*) as cnt FROM users WHERE last_active_date = ?', (today,))
    active_today = cursor.fetchone()['cnt'] or 0
    
    cursor.execute('SELECT COUNT(*) as cnt FROM users WHERE last_active_date >= ?', (week_ago,))
    active_7d = cursor.fetchone()['cnt'] or 0
    
    # 4. Total cards across all users
    cursor.execute('SELECT COUNT(*) as total FROM cards')
    total_cards = cursor.fetchone()['total'] or 0
    
    cursor.execute("SELECT COUNT(*) as cnt FROM cards WHERE status = 'known'")
    known_cards = cursor.fetchone()['cnt'] or 0
    
    cursor.execute("SELECT COUNT(*) as cnt FROM cards WHERE status = 'learning' OR status IS NULL")
    learning_cards = cursor.fetchone()['cnt'] or 0
    
    avg_cards_per_user = round(total_cards / max(1, total_users), 1)
    
    # 5. Full users list with progress details & languages
    cursor.execute('''
        SELECT 
            u.user_id,
            u.username,
            u.full_name,
            u.created_at,
            u.last_active_date,
            u.streak_days,
            u.level,
            COALESCE(u.native_lang, 'ru') as native_lang,
            COALESCE(u.target_lang, 'en') as target_lang,
            COUNT(c.id) as user_total_cards,
            SUM(CASE WHEN c.status = 'known' THEN 1 ELSE 0 END) as user_known_cards,
            SUM(CASE WHEN c.status = 'learning' OR c.status IS NULL THEN 1 ELSE 0 END) as user_learning_cards
        FROM users u
        LEFT JOIN cards c ON u.user_id = c.user_id
        GROUP BY u.user_id
        ORDER BY u.created_at DESC
    ''')
    users_rows = cursor.fetchall()
    users_list = []
    for r in users_rows:
        u_name = r['username'] or ''
        f_name = r['full_name'] or 'Без имени'
        n_l = r['native_lang'] or 'ru'
        t_l = r['target_lang'] or 'en'
        users_list.append({
            'user_id': r['user_id'],
            'username': u_name,
            'full_name': f_name,
            'display_title': f"@{u_name}" if u_name else f_name,
            'created_at': str(r['created_at'])[:16] if r['created_at'] else '',
            'last_active_date': r['last_active_date'] or '',
            'streak_days': r['streak_days'] or 1,
            'level': r['level'] or 'B1 Intermediate',
            'native_lang': n_l,
            'target_lang': t_l,
            'lang_pair_str': f"{SUPPORTED_LANGS.get(n_l, {}).get('flag', '🇷🇺')} ➔ {SUPPORTED_LANGS.get(t_l, {}).get('flag', '🇬🇧')} {SUPPORTED_LANGS.get(t_l, {}).get('short', 'EN')}",
            'total_cards': r['user_total_cards'] or 0,
            'known_cards': r['user_known_cards'] or 0,
            'learning_cards': r['user_learning_cards'] or 0,
        })
        
    # 6. Language Breakdown
    cursor.execute('''
        SELECT 
            COALESCE(target_lang, 'en') as lang_code,
            COUNT(*) as user_count
        FROM users
        GROUP BY lang_code
    ''')
    lang_user_counts = {r['lang_code']: r['user_count'] for r in cursor.fetchall()}

    cursor.execute('''
        SELECT 
            COALESCE(target_lang, 'en') as lang_code,
            COUNT(*) as card_count
        FROM cards
        GROUP BY lang_code
    ''')
    lang_card_counts = {r['lang_code']: r['card_count'] for r in cursor.fetchall()}

    language_stats = []
    for code, meta in SUPPORTED_LANGS.items():
        language_stats.append({
            'code': code,
            'name': meta['name'],
            'flag': meta['flag'],
            'short': meta['short'],
            'speech_code': meta['speech_code'],
            'users_count': lang_user_counts.get(code, 0),
            'cards_count': lang_card_counts.get(code, 0)
        })
    language_stats.sort(key=lambda x: (x['users_count'], x['cards_count']), reverse=True)
        
    # 7. 7-day activity dynamic
    daily_stats = []
    for i in range(6, -1, -1):
        target_dt = datetime.now() - timedelta(days=i)
        d = target_dt.strftime('%Y-%m-%d')
        cursor.execute('SELECT COUNT(*) as cnt FROM users WHERE DATE(created_at) = ?', (d,))
        new_cnt = cursor.fetchone()['cnt'] or 0
        cursor.execute('SELECT COUNT(*) as cnt FROM users WHERE last_active_date = ?', (d,))
        act_cnt = cursor.fetchone()['cnt'] or 0
        daily_stats.append({
            'date': d,
            'label': target_dt.strftime('%d.%m'),
            'new_users': new_cnt,
            'active_users': act_cnt
        })
        
    conn.close()
    
    return {
        'total_users': total_users,
        'new_users_today': new_users_today,
        'new_users_7d': new_users_7d,
        'active_today': active_today,
        'active_7d': active_7d,
        'total_cards': total_cards,
        'known_cards': known_cards,
        'learning_cards': learning_cards,
        'avg_cards_per_user': avg_cards_per_user,
        'users_list': users_list,
        'language_stats': language_stats,
        'daily_stats': daily_stats
    }

def generate_analytics_excel_file(output_path: str = None) -> str:
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    
    if not output_path:
        output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'WOW_English_Analytics.xlsx')
        
    data = get_admin_analytics()
    wb = openpyxl.Workbook()
    
    # Sheet 1: Общая сводка и Языки
    ws1 = wb.active
    ws1.title = "Сводка & Языки"
    ws1.views.sheetView[0].showGridLines = True
    
    header_fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    kpi_fill = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")
    kpi_val_font = Font(name="Calibri", size=18, bold=True, color="0F172A")
    kpi_lbl_font = Font(name="Calibri", size=10, color="64748B")
    thin_border = Border(
        left=Side(style='thin', color='E2E8F0'),
        right=Side(style='thin', color='E2E8F0'),
        top=Side(style='thin', color='E2E8F0'),
        bottom=Side(style='thin', color='E2E8F0')
    )
    
    # Title
    ws1.merge_cells("A1:F1")
    ws1["A1"] = "📊 WOW LANGUAGES — АНАЛИТИКА & МУЛЬТИЯЗЫЧНЫЕ МЕТРИКИ"
    ws1["A1"].font = Font(name="Calibri", size=15, bold=True, color="1E293B")
    ws1["A1"].alignment = Alignment(vertical="center")
    ws1.row_dimensions[1].height = 32
    
    ws1["A2"] = f"Сформировано: {datetime.now().strftime('%d.%m.%Y %H:%M')}"
    ws1["A2"].font = Font(name="Calibri", size=10, italic=True, color="64748B")
    
    # KPI Grid
    kpis = [
        ("Всего пользователей", data['total_users'], "A4", "B4"),
        ("Новых за 7 дней", data['new_users_7d'], "C4", "D4"),
        ("Активных сегодня (DAU)", data['active_today'], "E4", "F4"),
        ("Всего карточек в базе", data['total_cards'], "A6", "B6"),
        ("Выучено слов (Знаю)", data['known_cards'], "C6", "D6"),
        ("В процессе (Учу)", data['learning_cards'], "E6", "F6")
    ]
    
    for lbl, val, c1, c2 in kpis:
        col1 = c1[0]
        row = int(c1[1])
        ws1[c1] = val
        ws1[c1].font = kpi_val_font
        ws1[c1].alignment = Alignment(horizontal="center", vertical="center")
        ws1[c1].fill = kpi_fill
        
        lbl_cell = f"{col1}{row+1}"
        ws1[lbl_cell] = lbl
        ws1[lbl_cell].font = kpi_lbl_font
        ws1[lbl_cell].alignment = Alignment(horizontal="center", vertical="center")
        ws1[lbl_cell].fill = kpi_fill
        
    ws1.row_dimensions[4].height = 26
    ws1.row_dimensions[5].height = 18
    ws1.row_dimensions[6].height = 26
    ws1.row_dimensions[7].height = 18
    
    # Language Breakdown Subtable on Sheet 1
    ws1.cell(row=9, column=1, value="🌍 РАСПРЕДЕЛЕНИЕ ПО ИЗУЧАЕМЫМ ЯЗЫКАМ").font = Font(name="Calibri", size=12, bold=True, color="1E293B")
    
    lang_headers = ["Язык", "Флаг", "Код", "Количество учеников", "Всего карточек"]
    ws1.row_dimensions[10].height = 22
    for col_idx, h in enumerate(lang_headers, 1):
        cell = ws1.cell(row=10, column=col_idx, value=h)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
        
    l_row = 11
    for l in data.get('language_stats', []):
        ws1.row_dimensions[l_row].height = 20
        row_vals = [l['name'], l['flag'], l['short'], l['users_count'], l['cards_count']]
        for col_idx, val in enumerate(row_vals, 1):
            c = ws1.cell(row=l_row, column=col_idx, value=val)
            c.border = thin_border
            c.font = Font(name="Calibri", size=11)
            if col_idx in [2, 3, 4, 5]:
                c.alignment = Alignment(horizontal="center", vertical="center")
            else:
                c.alignment = Alignment(horizontal="left", vertical="center")
        l_row += 1
    
    # Sheet 2: Список пользователей
    ws2 = wb.create_sheet(title="Ученики (Users)")
    ws2.views.sheetView[0].showGridLines = True
    
    headers = [
        "ID", "Telegram Ник", "Имя", "Языковая пара", "Дата регистрации", 
        "Последний визит", "Серия (дней)", "Всего карточек", 
        "Выучено (Знаю)", "В процессе (Учу)"
    ]
    
    ws2.row_dimensions[1].height = 26
    for col_idx, h in enumerate(headers, 1):
        cell = ws2.cell(row=1, column=col_idx, value=h)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
        
    row_num = 2
    for u in data['users_list']:
        ws2.row_dimensions[row_num].height = 20
        row_data = [
            u['user_id'],
            f"@{u['username']}" if u['username'] else "—",
            u['full_name'],
            u.get('lang_pair_str', '🇷🇺 ➔ 🇬🇧 EN'),
            u['created_at'],
            u['last_active_date'],
            u['streak_days'],
            u['total_cards'],
            u['known_cards'],
            u['learning_cards']
        ]
        for col_idx, val in enumerate(row_data, 1):
            c = ws2.cell(row=row_num, column=col_idx, value=val)
            c.border = thin_border
            c.font = Font(name="Calibri", size=11)
            if col_idx in [1, 4, 5, 6, 7, 8, 9, 10]:
                c.alignment = Alignment(horizontal="center", vertical="center")
            else:
                c.alignment = Alignment(horizontal="left", vertical="center")
        row_num += 1
        
    for ws in [ws1, ws2]:
        for col in ws.columns:
            max_len = max(len(str(cell.value or '')) for cell in col)
            col_letter = openpyxl.utils.get_column_letter(col[0].column)
            ws.column_dimensions[col_letter].width = max(max_len + 4, 12)
            
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    wb.save(output_path)
    return output_path

# --- STUDY GROUPS & TRAINER MODULE ---

def ensure_user_groups(user_id: int, target_lang: str = 'en', native_lang: str = 'ru'):
    """
    Ensures user cards are organized into ordered groups of 10 phrases.
    Dynamically creates new groups, assigns group_id to all cards, cleans up excess groups,
    and returns the complete list of groups with real-time aggregated stats.
    """
    t_lang = target_lang if target_lang in SUPPORTED_LANGS else 'en'
    n_lang = native_lang if native_lang in SUPPORTED_LANGS else 'ru'
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get all cards for user and language ordered by ID
    cursor.execute('''
        SELECT id, group_id, trainer_status 
        FROM cards 
        WHERE user_id = ? AND (target_lang = ? OR target_lang IS NULL) AND (native_lang = ? OR native_lang IS NULL)
        ORDER BY id ASC
    ''', (user_id, t_lang, n_lang))
    cards = cursor.fetchall()
    
    if not cards:
        cursor.execute('DELETE FROM study_groups WHERE user_id = ? AND target_lang = ? AND native_lang = ?', (user_id, t_lang, n_lang))
        conn.commit()
        conn.close()
        return []

    # Get existing groups for user
    cursor.execute('''
        SELECT * FROM study_groups 
        WHERE user_id = ? AND target_lang = ? AND native_lang = ?
        ORDER BY group_order ASC
    ''', (user_id, t_lang, n_lang))
    existing_groups = [dict(g) for g in cursor.fetchall()]
    group_map_by_order = {g['group_order']: g for g in existing_groups}
    
    chunk_size = 10
    total_chunks = (len(cards) + chunk_size - 1) // chunk_size
    
    for chunk_idx in range(total_chunks):
        order_num = chunk_idx + 1
        chunk_cards = cards[chunk_idx * chunk_size : (chunk_idx + 1) * chunk_size]
        
        # Check or create group
        if order_num not in group_map_by_order:
            default_name = f"{order_num} группа"
            cursor.execute('''
                INSERT INTO study_groups (user_id, group_order, name, status, target_lang, native_lang)
                VALUES (?, ?, ?, 'new', ?, ?)
            ''', (user_id, order_num, default_name, t_lang, n_lang))
            group_id = cursor.lastrowid
            group_map_by_order[order_num] = {
                'id': group_id,
                'user_id': user_id,
                'group_order': order_num,
                'name': default_name,
                'status': 'new',
                'target_lang': t_lang,
                'native_lang': n_lang
            }
        else:
            group_id = group_map_by_order[order_num]['id']
            
        # Assign group_id to cards in chunk if needed
        for c in chunk_cards:
            if c['group_id'] != group_id:
                cursor.execute('UPDATE cards SET group_id = ? WHERE id = ?', (group_id, c['id']))
                
    # Remove any excess empty groups if cards were deleted
    for g in existing_groups:
        if g['group_order'] > total_chunks:
            cursor.execute('DELETE FROM study_groups WHERE id = ?', (g['id'],))
            
    conn.commit()
    
    # Query final active groups
    cursor.execute('''
        SELECT * FROM study_groups 
        WHERE user_id = ? AND target_lang = ? AND native_lang = ?
        ORDER BY group_order ASC
    ''', (user_id, t_lang, n_lang))
    group_rows = cursor.fetchall()
    
    result = []
    for g in group_rows:
        g_dict = dict(g)
        cursor.execute('''
            SELECT id, phrase_en, phrase_ru, category, status, trainer_status, group_id 
            FROM cards 
            WHERE group_id = ? AND user_id = ?
            ORDER BY id ASC
        ''', (g_dict['id'], user_id))
        cards_list = [dict(c) for c in cursor.fetchall()]
        
        green_count = sum(1 for c in cards_list if c.get('trainer_status') == 'green')
        red_count = sum(1 for c in cards_list if c.get('trainer_status') == 'red')
        neutral_count = sum(1 for c in cards_list if not c.get('trainer_status') or c.get('trainer_status') == 'neutral')
        total_cards = len(cards_list)
        
        # Determine reactive status
        curr_status = g_dict.get('status', 'new')
        if total_cards > 0 and green_count == total_cards:
            derived_status = 'mastered'
        elif red_count > 0 or (green_count > 0 and green_count < total_cards) or curr_status == 'in_progress':
            derived_status = 'in_progress'
        else:
            derived_status = curr_status if curr_status in ['new', 'in_progress', 'mastered'] else 'new'
            
        if derived_status != curr_status:
            cursor.execute('UPDATE study_groups SET status = ? WHERE id = ?', (derived_status, g_dict['id']))
            conn.commit()
            g_dict['status'] = derived_status
            
        g_dict['total_cards'] = total_cards
        g_dict['green_count'] = green_count
        g_dict['red_count'] = red_count
        g_dict['neutral_count'] = neutral_count
        g_dict['cards'] = cards_list
        result.append(g_dict)
        
    conn.close()
    return result

def get_user_groups(user_id: int, target_lang: str = 'en', native_lang: str = 'ru'):
    """
    Returns full list of groups with their cards and aggregated statuses.
    Always invokes ensure_user_groups to maintain absolute synchronization.
    """
    return ensure_user_groups(user_id, target_lang=target_lang, native_lang=native_lang)

def update_group_name(group_id: int, new_name: str, user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    clean_name = new_name.strip() if new_name else ""
    if not clean_name:
        conn.close()
        return False
    cursor.execute('UPDATE study_groups SET name = ? WHERE id = ? AND user_id = ?', (clean_name, group_id, user_id))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0

def update_group_status(group_id: int, new_status: str, user_id: int):
    """new_status: 'new', 'in_progress', 'mastered'"""
    if new_status not in ['new', 'in_progress', 'mastered']:
        return False
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE study_groups SET status = ? WHERE id = ? AND user_id = ?', (new_status, group_id, user_id))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0

def reset_group_result(group_id: int, user_id: int):
    """
    Resets all cards in group to 'neutral' and returns group status to 'new' (dark).
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE cards SET trainer_status = "neutral" WHERE group_id = ? AND user_id = ?', (group_id, user_id))
    cursor.execute('UPDATE study_groups SET status = "new" WHERE id = ? AND user_id = ?', (group_id, user_id))
    conn.commit()
    conn.close()
    return True

def update_card_trainer_status(card_id: int, trainer_status: str, user_id: int):
    """
    trainer_status: 'green', 'red', 'neutral'
    Returns { status: 'ok', card_id, trainer_status, group_completed: { id, name, group_order } or None }
    """
    if trainer_status not in ['green', 'red', 'neutral']:
        return None
        
    conn = get_connection()
    cursor = conn.cursor()
    
    # Also update card status if green -> 'known'
    if trainer_status == 'green':
        cursor.execute('''
            UPDATE cards 
            SET trainer_status = ?, status = 'known', repetitions = MAX(repetitions, 1)
            WHERE id = ? AND user_id = ?
        ''', (trainer_status, card_id, user_id))
    else:
        cursor.execute('''
            UPDATE cards 
            SET trainer_status = ?
            WHERE id = ? AND user_id = ?
        ''', (trainer_status, card_id, user_id))
        
    # Check if card has group_id
    cursor.execute('SELECT group_id FROM cards WHERE id = ? AND user_id = ?', (card_id, user_id))
    c_row = cursor.fetchone()
    group_completed = None
    
    if c_row and c_row['group_id']:
        gid = c_row['group_id']
        # Fetch group cards
        cursor.execute('SELECT trainer_status FROM cards WHERE group_id = ? AND user_id = ?', (gid, user_id))
        g_cards = cursor.fetchall()
        total_g = len(g_cards)
        greens_g = sum(1 for gc in g_cards if gc['trainer_status'] == 'green')
        
        cursor.execute('SELECT id, name, group_order, status FROM study_groups WHERE id = ? AND user_id = ?', (gid, user_id))
        grp = cursor.fetchone()
        
        if total_g > 0 and greens_g == total_g and grp:
            if grp['status'] != 'mastered':
                cursor.execute('UPDATE study_groups SET status = "mastered" WHERE id = ?', (gid,))
                group_completed = {
                    'id': grp['id'],
                    'name': grp['name'],
                    'group_order': grp['group_order']
                }
        elif grp and grp['status'] == 'new' and (trainer_status in ['red', 'green']):
            cursor.execute('UPDATE study_groups SET status = "in_progress" WHERE id = ?', (gid,))
            
    conn.commit()
    conn.close()
    return {
        'card_id': card_id,
        'trainer_status': trainer_status,
        'group_completed': group_completed
    }

def get_red_cards(user_id: int, target_lang: str = 'en', native_lang: str = 'ru'):
    t_lang = target_lang if target_lang in SUPPORTED_LANGS else 'en'
    n_lang = native_lang if native_lang in SUPPORTED_LANGS else 'ru'
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT c.id, c.phrase_en, c.phrase_ru, c.category, c.status, c.trainer_status, c.group_id, g.name as group_name, g.group_order
        FROM cards c
        LEFT JOIN study_groups g ON c.group_id = g.id
        WHERE c.user_id = ? AND (c.target_lang = ? OR c.target_lang IS NULL) AND (c.native_lang = ? OR c.native_lang IS NULL)
          AND c.trainer_status = 'red'
        ORDER BY c.id ASC
    ''', (user_id, t_lang, n_lang))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

