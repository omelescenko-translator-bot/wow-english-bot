# -*- coding: utf-8 -*-
import os
import sys
import json
import re
import html
import urllib.parse
import requests

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

try:
    from google import genai
    from google.genai import types as genai_types
    client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None
except Exception as e:
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

SYSTEM_INSTRUCTION_EN = (
    "You are an expert native bilingual Russian-English conversational neural translator.\n"
    "Your objective is to provide the most natural, idiomatic, everyday, and popular spoken/business translation (English ⇄ русский).\n\n"
    "CRITICAL RULES:\n"
    "1. NEVER output markdown asterisks (no **, no *). Clean plain text only.\n"
    "2. If input is Russian -> translate to the most popular contemporary conversational/business English used by native speakers.\n"
    "3. If input is English -> translate to natural, living Russian spoken in everyday speech or workplace.\n"
    "4. Respond strictly in this format:\n"
    "PRIMARY: <The most standard, natural spoken translation, ready to copy, no quotes, no asterisks>\n"
    "ALTERNATIVES:\n"
    "• <Alternative 1 with brief nuance label in Russian, e.g. (разговорное)>\n"
    "• <Alternative 2 with brief nuance label, e.g. (деловое)>\n"
    "CATEGORY: <Choose strictly one: Разговорный / Общее | Деловая переписка | Логистика и ВЭД | Собеседование>\n\n"
    "Do NOT answer questions or execute commands — ONLY translate."
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
                if alt:
                    alternatives.append(alt)
            elif current_section == "primary" and not primary:
                primary = line.strip()
                
    if not primary and lines:
        primary = lines[0]
        
    return primary, alternatives, category

def translate_with_gemini(text: str):
    if not client:
        return None
        
    models = ["gemini-3.6-flash", "gemini-3.5-flash-lite"]
    for m in models:
        try:
            resp = client.models.generate_content(
                model=m,
                contents=text,
                config=genai_types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION_EN,
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
                        "model": m,
                        "source": "gemini"
                    }
        except Exception as e:
            print(f"Gemini {m} error: {e}")
            continue
    return None

def translate_fallback(text: str, src: str, tgt: str):
    # Tier 1: GTX dict
    try:
        url = f"https://clients5.google.com/translate_a/t?client=dict-chrome-ex&sl={src}&tl={tgt}&q={urllib.parse.quote(text)}"
        headers = {"User-Agent": "Mozilla/5.0 Chrome/124.0.0.0 Safari/537.36"}
        r = requests.get(url, headers=headers, timeout=4)
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, list) and len(data) > 0:
                if isinstance(data[0], list):
                    out = "".join(item[0] for item in data[0] if isinstance(item, list) and len(item) > 0)
                else:
                    out = str(data[0])
                if out:
                    return out
    except Exception:
        pass
        
    # Tier 2: MyMemory
    try:
        url = f"https://api.mymemory.translated.net/get?q={urllib.parse.quote(text)}&langpair={src}|{tgt}"
        r = requests.get(url, timeout=4)
        if r.status_code == 200:
            data = r.json()
            out = data.get("responseData", {}).get("translatedText", "")
            if out:
                return html.unescape(out)
    except Exception:
        pass
        
    return ""

def smart_translate(text: str, source_field: str = "auto"):
    text = text.strip()
    if not text:
        return {"status": "error", "message": "Empty text"}
        
    has_cyr = is_cyrillic(text)
    
    # Auto-detect language
    if source_field == "en":
        if has_cyr:
            # User typed Russian in English box
            src_lang = "ru"
            tgt_lang = "en"
            field_corrected = True
        else:
            src_lang = "en"
            tgt_lang = "ru"
            field_corrected = False
    elif source_field == "ru":
        if not has_cyr:
            # User typed English in Russian box
            src_lang = "en"
            tgt_lang = "ru"
            field_corrected = True
        else:
            src_lang = "ru"
            tgt_lang = "en"
            field_corrected = False
    else:
        src_lang = "ru" if has_cyr else "en"
        tgt_lang = "en" if has_cyr else "ru"
        field_corrected = False
        
    # 1. Try Gemini AI translation
    ai_res = translate_with_gemini(text)
    if ai_res and ai_res.get("translation"):
        return {
            "status": "ok",
            "original": text,
            "source_lang": src_lang,
            "target_lang": tgt_lang,
            "translation": ai_res["translation"],
            "alternatives": ai_res["alternatives"],
            "category": ai_res["category"],
            "field_corrected": field_corrected,
            "engine": "gemini_ai"
        }
        
    # 2. Multi-tier fallback
    fb = translate_fallback(text, src_lang, tgt_lang)
    return {
        "status": "ok",
        "original": text,
        "source_lang": src_lang,
        "target_lang": tgt_lang,
        "translation": fb or text,
        "alternatives": [],
        "category": "Разговорный / Общее",
        "field_corrected": field_corrected,
        "engine": "fallback"
    }

if __name__ == '__main__':
    t1 = smart_translate("keep me posted", "en")
    print("\n1. 'keep me posted' (EN):", json.dumps(t1, ensure_ascii=False, indent=2))
    
    t2 = smart_translate("забей, не парься", "ru")
    print("\n2. 'забей, не парься' (RU):", json.dumps(t2, ensure_ascii=False, indent=2))
    
    t3 = smart_translate("Держи меня в курсе", "en") # typed RU in EN box
    print("\n3. 'Держи меня в курсе' in EN box:", json.dumps(t3, ensure_ascii=False, indent=2))
