# -*- coding: utf-8 -*-
import sys
try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

from fastapi.testclient import TestClient
from server import app
import json

client = TestClient(app)

def test_news_endpoint():
    print("=== Testing /api/trainer/news_context Endpoint ===")
    
    words_data = [
        {"id": 101, "phrase_en": "Keep me in the loop", "phrase_ru": "Держи меня в курсе"},
        {"id": 102, "phrase_en": "Lead time", "phrase_ru": "Срок поставки"},
        {"id": 103, "phrase_en": "Red carpet", "phrase_ru": "Красная дорожка"},
        {"id": 104, "phrase_en": "Cut delivery times", "phrase_ru": "Сократить сроки доставки"},
        {"id": 105, "phrase_en": "Deal with it", "phrase_ru": "Справиться с этим"}
    ]

    res = client.post("/api/trainer/news_context", json={
        "user_id": 466788167,
        "words": words_data,
        "target_lang": "en",
        "native_lang": "ru"
    })
    
    assert res.status_code == 200, f"Status code: {res.status_code}"
    data = res.json()
    assert data["status"] == "ok"
    assert "stories" in data
    stories = data["stories"]
    print(f"✅ Generated {len(stories)} stories for 5 words")
    
    covered_ids = set()
    for s in stories:
        print(f"\n📰 Story [{s['topic']}] '{s['title']}' (Source: {s['source']})")
        print(f"Target words: {[w['phrase_target'] for w in s['target_words']]}")
        print(f"Text preview: {s['text_target'][:120]}...")
        print(f"Native preview: {s['text_native'][:120]}...")
        for wid in s.get("word_ids", []):
            covered_ids.add(wid)

    assert len(covered_ids) == len(words_data), f"Expected all {len(words_data)} words covered, but got {len(covered_ids)}"
    print(f"\n✅ 100% of words covered across generated news stories ({len(covered_ids)}/{len(words_data)})!")

if __name__ == "__main__":
    test_news_endpoint()
