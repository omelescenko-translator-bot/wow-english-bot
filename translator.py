# -*- coding: utf-8 -*-
import os
import re
import html
import urllib.parse
import requests
import logging

try:
    from config import GEMINI_API_KEY
except Exception:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

logger = logging.getLogger(__name__)

# Initialize GenAI client only if valid key provided
client = None
try:
    from google import genai
    from google.genai import types as genai_types
    api_key = os.getenv("GEMINI_API_KEY", GEMINI_API_KEY)
    if api_key and (api_key.startswith("AIzaSy") or len(api_key) > 30 and not api_key.startswith("AQ.")):
        client = genai.Client(api_key=api_key)
except Exception as e:
    logger.warning(f"Failed to initialize GenAI Client: {e}")
    client = None

def is_cyrillic(text: str) -> bool:
    return bool(re.search(r'[\u0400-\u04FF]', text))

def clean_markdown_asterisks(text: str) -> str:
    if not text:
        return ""
    t = text
    t = re.sub(r'\*\*(.*?)\*\*', r'\1', t)
    t = re.sub(r'\*(.*?)\*', r'\1', t)
    t = re.sub(r'__(.*?)__', r'\1', t)
    t = re.sub(r'_(.*?)_', r'\1', t)
    t = t.replace("**", "").replace("*", "").replace("`", "")
    return t.strip()

LANGUAGE_NAMES = {
    'ru': 'Russian (Русский)',
    'uk': 'Ukrainian (Українська)',
    'en': 'English (Английский)',
    'es': 'Spanish (Испанский)',
    'fr': 'French (Французский)',
    'de': 'German (Немецкий)',
    'it': 'Italian (Итальянский)',
    'sl': 'Slovenian (Словенский)'
}

def build_system_instruction(native_lang: str = "ru", target_lang: str = "en") -> str:
    n_name = LANGUAGE_NAMES.get(native_lang, 'Russian')
    t_name = LANGUAGE_NAMES.get(target_lang, 'English')
    return (
        f"You are an elite multilingual translator and language coach specializing in {n_name} ⇄ {t_name}.\n"
        f"Your objective is to provide the most natural, accurate, contemporary, and idiomatic translation.\n\n"
        "CRITICAL RULES:\n"
        "1. NEVER output markdown asterisks (no **, no *). Clean plain text only.\n"
        f"2. If input is {t_name} -> translate to natural, living, grammatically flawless {n_name}.\n"
        f"3. If input is {n_name} -> translate to the most natural, contemporary spoken or business {t_name}.\n"
        "4. Respond strictly in this format:\n"
        "PRIMARY: <The most natural, grammatically correct and polished translation>\n"
        "ALTERNATIVES:\n"
        "• <Alternative 1 with brief nuance label, e.g. (разговорное)>\n"
        "• <Alternative 2 with brief nuance label, e.g. (деловое / более формальное)>\n"
        "CATEGORY: <Choose strictly one: Разговорный / Общее | Деловая переписка | Логистика и ВЭД | Собеседование>\n\n"
        "Do NOT answer questions or add explanations — ONLY output the specified format."
    )

def parse_ai_response(raw_text: str):
    clean = clean_markdown_asterisks(raw_text)
    primary = ""
    alternatives = []
    category = "Разговорный / Общее"
    
    lines = [l.strip() for l in clean.split("\n") if l.strip()]
    current_section = None
    
    for line in lines:
        if line.startswith("PRIMARY:"):
            primary = line.replace("PRIMARY:", "").strip()
            current_section = "primary"
        elif line.startswith("ALTERNATIVES:"):
            current_section = "alternatives"
        elif line.startswith("CATEGORY:"):
            category = line.replace("CATEGORY:", "").strip()
            current_section = "category"
        else:
            if current_section == "alternatives":
                alt = line.lstrip("•-* ").strip()
                if alt and alt.lower() != "none" and len(alt) > 2:
                    alternatives.append(alt)
            elif current_section == "primary" and not primary:
                primary = line.strip()
                
    if not primary and lines:
        primary = lines[0]
        
    return primary, alternatives, category

import concurrent.futures

_executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)

def _call_gemini_single(model_name: str, text: str, native_lang: str = "ru", target_lang: str = "en"):
    if not client:
        return None
    try:
        instruction = build_system_instruction(native_lang, target_lang)
        resp = client.models.generate_content(
            model=model_name,
            contents=text,
            config=genai_types.GenerateContentConfig(
                system_instruction=instruction,
                temperature=0.2,
            )
        )
        if resp and resp.text:
            prim, alts, cat = parse_ai_response(resp.text.strip())
            if prim:
                return {
                    "translation": prim,
                    "alternatives": alts,
                    "category": cat,
                    "model": model_name,
                    "source": "gemini"
                }
    except Exception as e:
        logger.warning(f"Gemini {model_name} error: {e}")
    return None

def translate_with_gemini(text: str, native_lang: str = "ru", target_lang: str = "en", timeout_sec: float = 2.5):
    if not client:
        return None
        
    models = ["gemini-3.5-flash-lite", "gemini-3.5-flash"]
    for m in models:
        try:
            future = _executor.submit(_call_gemini_single, m, text, native_lang, target_lang)
            res = future.result(timeout=timeout_sec)
            if res:
                return res
        except concurrent.futures.TimeoutError:
            logger.warning(f"Gemini model {m} timed out after {timeout_sec}s")
            continue
        except Exception as e:
            logger.warning(f"Gemini execution error on {m}: {e}")
            continue
    return None


def translate_fallback_gtx(text: str, src: str, tgt: str):
    try:
        url = f"https://clients5.google.com/translate_a/t?client=dict-chrome-ex&sl={src}&tl={tgt}&q={urllib.parse.quote(text)}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        r = requests.get(url, headers=headers, timeout=4)
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, list) and len(data) > 0:
                if isinstance(data[0], list):
                    out = "".join(item[0] for item in data[0] if isinstance(item, list) and len(item) > 0)
                else:
                    out = str(data[0])
                if out:
                    return clean_markdown_asterisks(out)
    except Exception:
        pass
    return ""

def translate_fallback_mymemory(text: str, src: str, tgt: str):
    try:
        url = f"https://api.mymemory.translated.net/get?q={urllib.parse.quote(text)}&langpair={src}|{tgt}"
        r = requests.get(url, timeout=4)
        if r.status_code == 200:
            data = r.json()
            out = data.get("responseData", {}).get("translatedText", "")
            if out and "MYMEMORY WARNING" not in out.upper():
                return clean_markdown_asterisks(html.unescape(out))
    except Exception:
        pass
    return ""

def auto_detect_category(text_target: str, text_native: str) -> str:
    combined = f"{text_target} {text_native}".lower()
    
    logistics_keywords = [
        'shipment', 'customs', 'cargo', 'delivery', 'warehouse', 'freight', 'carrier',
        'lead time', 'bill of lading', 'tracking', 'logistics', 'dispatch', 'груз',
        'тамож', 'доставк', 'склад', 'поставк', 'накладн', 'логистик', 'отгруз', 'контейнер',
        'tovorno', 'carina', 'dostava', 'skladišče', 'logistika', 'dobava', 'pošiljka'
    ]
    business_keywords = [
        'loop', 'posted', 'meeting', 'agenda', 'follow up', 'regards', 'attached',
        'proposal', 'contract', 'deadline', 'client', 'schedule', 'quarter', 'invoice',
        'в курсе', 'встреч', 'письм', 'вложени', 'договор', 'сроки', 'клиент', 'переговор', 'отчет',
        'pogodba', 'sestanek', 'rok', 'stranka', 'poročilo', 'ponudba'
    ]
    interview_keywords = [
        'strength', 'weakness', 'experience', 'background', 'hire', 'salary',
        'qualification', 'interview', 'career', 'resume', 'skills', 'responsibilities',
        'собеседован', 'опыт', 'зарплат', 'резюме', 'навык', 'сильная сторона', 'ваканси',
        'razgovor', 'izkušnje', 'plača', 'življenjepis', 'znanje', 'zaposlitev'
    ]
    
    for kw in logistics_keywords:
        if kw in combined:
            return "Логистика и ВЭД"
    for kw in business_keywords:
        if kw in combined:
            return "Деловая переписка"
    for kw in interview_keywords:
        if kw in combined:
            return "Собеседование"
            
    return "Разговорный / Общее"

def smart_translate(text: str, source_field: str = "auto", native_lang: str = "ru", target_lang: str = "en") -> dict:
    text = text.strip()
    if not text:
        return {"status": "error", "message": "Пустой текст"}
        
    n_lang = native_lang if native_lang in LANGUAGE_NAMES else "ru"
    t_lang = target_lang if target_lang in LANGUAGE_NAMES else "en"
    
    has_cyr = is_cyrillic(text)
    
    # Determine direction
    if source_field in ["target", "en"]:
        if n_lang == "ru" and has_cyr:
            src_lang = n_lang
            tgt_lang = t_lang
            field_corrected = True
        else:
            src_lang = t_lang
            tgt_lang = n_lang
            field_corrected = False
    elif source_field in ["native", "ru"]:
        if n_lang == "ru" and not has_cyr:
            src_lang = t_lang
            tgt_lang = n_lang
            field_corrected = True
        else:
            src_lang = n_lang
            tgt_lang = t_lang
            field_corrected = False
    else:
        if n_lang == "ru":
            src_lang = "ru" if has_cyr else t_lang
            tgt_lang = t_lang if has_cyr else "ru"
        else:
            src_lang = n_lang
            tgt_lang = t_lang
        field_corrected = False
        
    # 1. Try Gemini AI Translation
    ai_res = translate_with_gemini(text, native_lang=n_lang, target_lang=t_lang)
    if ai_res and ai_res.get("translation"):
        cat = ai_res.get("category") or auto_detect_category(
            text if src_lang == t_lang else ai_res["translation"],
            ai_res["translation"] if src_lang == t_lang else text
        )
        return {
            "status": "ok",
            "original": text,
            "source_lang": src_lang,
            "target_lang": tgt_lang,
            "translation": ai_res["translation"],
            "alternatives": ai_res.get("alternatives", []),
            "category": cat,
            "field_corrected": field_corrected,
            "engine": "gemini_ai"
        }
        
    # 2. Multi-tier Fallback
    fallback_trans = translate_fallback_gtx(text, src_lang, tgt_lang)
    if not fallback_trans:
        fallback_trans = translate_fallback_mymemory(text, src_lang, tgt_lang)
        
    final_trans = fallback_trans if fallback_trans else text
    cat = auto_detect_category(
        text if src_lang == t_lang else final_trans,
        final_trans if src_lang == t_lang else text
    )
    
    return {
        "status": "ok",
        "original": text,
        "source_lang": src_lang,
        "target_lang": tgt_lang,
        "translation": final_trans,
        "alternatives": [],
        "category": cat,
        "field_corrected": field_corrected,
        "engine": "fallback"
    }

def categorize_user_vocabulary(cards: list, native_lang: str = "ru", target_lang: str = "en") -> dict:
    """
    Groups a user's vocabulary (when >= 30 phrases) into 3-5 concise, natural categories in native_lang.
    Returns: {"categories": [...], "card_categories": {"<card_id>": "<category_name>"}}
    """
    if not cards or len(cards) < 30:
        return {"categories": [], "card_categories": {}}

    n_name = LANGUAGE_NAMES.get(native_lang, 'Russian')
    t_name = LANGUAGE_NAMES.get(target_lang, 'English')

    # Prepare sample list of cards (up to 60 cards for concise token usage)
    phrases_sample = []
    for c in cards[:60]:
        phrases_sample.append(f"ID {c['id']}: {c.get('phrase_ru', '')} — {c.get('phrase_en', '')}")
    sample_text = "\n".join(phrases_sample)

    prompt = (
        f"You are an expert language learning curriculum designer.\n"
        f"Analyze these {len(phrases_sample)} vocabulary flashcards for a user learning {t_name} from {n_name}.\n"
        f"Group all phrases into exactly 3 to 5 concise, practical, human-friendly topic categories in {n_name} "
        f"(for example: 'Разговорные фразы', 'Работа и созвоны', 'Путешествия и транспорт', 'Покупки и кафе', 'Эмоции и мысли').\n\n"
        f"Flashcards list:\n{sample_text}\n\n"
        f"Respond STRICTLY with a valid JSON object in this exact format (no markdown, no backticks):\n"
        f"{{\n"
        f'  "categories": ["Category 1", "Category 2", "Category 3"],\n'
        f'  "card_categories": {{\n'
        f'    "1": "Category 1",\n'
        f'    "2": "Category 2"\n'
        f"  }}\n"
        f"}}"
    )

    if client:
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=genai_types.GenerateContentConfig(
                    temperature=0.3,
                    max_output_tokens=2000,
                )
            )
            raw_text = response.text.strip()
            if raw_text.startswith("```"):
                raw_text = re.sub(r'^```(?:json)?\s*', '', raw_text)
                raw_text = re.sub(r'\s*```$', '', raw_text)
            import json
            data = json.loads(raw_text.strip())
            if isinstance(data, dict) and "categories" in data:
                return data
        except Exception as e:
            logger.warning(f"Gemini categorization failed: {e}")

    # Heuristic fallback categories in native language
    default_cats = {
        'ru': ["Разговорный", "Деловая переписка", "Логистика и транспорт", "Повседневное"],
        'uk': ["Розмовна", "Ділове листування", "Логістика та транспорт", "Повсякденне"],
        'en': ["Conversational", "Business & Email", "Logistics & Travel", "Daily Life"],
        'sl': ["Pogovorno", "Poslovna sporočila", "Logistika in potovanja", "Vsakdanje"],
        'es': ["Conversación", "Negocios y correo", "Logística y viajes", "Vida cotidiana"],
        'de': ["Gespräche", "Geschäftskorrespondenz", "Logistik & Reisen", "Alltag"],
        'fr': ["Conversation", "Affaires et courriels", "Logistique et voyages", "Vie quotidienne"],
        'it': ["Conversazione", "Affari ed email", "Logistica e viaggi", "Vita quotidiana"]
    }
    cats = default_cats.get(native_lang, default_cats['ru'])
    card_map = {}
    for idx, c in enumerate(cards):
        card_map[str(c['id'])] = cats[idx % len(cats)]
    return {"categories": cats, "card_categories": card_map}
