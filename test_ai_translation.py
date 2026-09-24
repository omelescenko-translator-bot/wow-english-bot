# -*- coding: utf-8 -*-
import os
import json
import re
from google import genai

key = os.getenv('GEMINI_API_KEY', '')
client = genai.Client(api_key=key) if key else None

def is_cyrillic(text: str) -> bool:
    return bool(re.search(r'[\u0400-\u04FF]', text))

def translate_ai(text: str):
    text = text.strip()
    if not text:
        return None
        
    detected_cyr = is_cyrillic(text)
    src_lang = "ru" if detected_cyr else "en"
    tgt_lang = "en" if detected_cyr else "ru"
    
    prompt = f"""Ты эксперт-лингвист и носитель живого современного разговорного английского и русского языков.
Твоя задача — перевести слово или фразу так, как РЕАЛЬНО говорят носители языка в повседневной жизни, живой разговорной речи или на работе (самый популярный, естественный и идиоматичный вариант, без книжного буквализма и калек).

Входной текст: "{text}"
Определенный язык ввода: {src_lang}. Переведи на: {tgt_lang}.

Ответь СТРОГО в формате JSON:
{{
  "source_lang": "{src_lang}",
  "target_lang": "{tgt_lang}",
  "translation": "основной самый популярный разговорный перевод",
  "alternatives": ["альтернатива 1", "альтернатива 2"],
  "category": "Разговорный / Общее"
}}

Категория: одна из "Разговорный / Общее", "Деловая переписка", "Логистика и ВЭД", "Собеседование".
"""

    models_to_try = ['gemini-3.6-flash', 'gemini-3.5-flash-lite']
    for m in models_to_try:
        try:
            interaction = client.interactions.create(
                model=m,
                input=prompt,
                response_format="json"
            )
            txt = interaction.output_text.strip()
            if '```json' in txt:
                txt = txt.split('```json')[1].split('```')[0].strip()
            elif '```' in txt:
                txt = txt.split('```')[1].split('```')[0].strip()
            data = json.loads(txt)
            data["model_used"] = m
            return data
        except Exception as e:
            try:
                # without response_format if not supported
                interaction = client.interactions.create(
                    model=m,
                    input=prompt
                )
                txt = interaction.output_text.strip()
                if '```json' in txt:
                    txt = txt.split('```json')[1].split('```')[0].strip()
                elif '```' in txt:
                    txt = txt.split('```')[1].split('```')[0].strip()
                data = json.loads(txt)
                data["model_used"] = m
                return data
            except Exception as e2:
                print(f"Error {m}: {e2}")
                continue
    return None

if __name__ == '__main__':
    res = translate_ai("keep me posted")
    print("EN -> RU:", res)
    res2 = translate_ai("забей, не парься")
    print("RU -> EN:", res2)
