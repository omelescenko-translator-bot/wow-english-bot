# -*- coding: utf-8 -*-
import sys
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

from fastapi.testclient import TestClient
from server import app
import json

client = TestClient(app)

def run_tests():
    print("=== Testing /api/translate Endpoint ===")
    
    # 1. EN -> RU conversational
    res1 = client.post("/api/translate", json={"text": "Keep me in the loop", "source_field": "en"})
    print("\n1. 'Keep me in the loop' (EN):")
    print(json.dumps(res1.json(), ensure_ascii=False, indent=2))
    assert res1.status_code == 200
    assert res1.json()["status"] == "ok"
    assert "translation" in res1.json()

    # 2. RU -> EN conversational
    res2 = client.post("/api/translate", json={"text": "По рукам, договорились!", "source_field": "ru"})
    print("\n2. 'По рукам, договорились!' (RU):")
    print(json.dumps(res2.json(), ensure_ascii=False, indent=2))
    assert res2.status_code == 200
    assert res2.json()["status"] == "ok"

    # 3. User typed Russian in English box
    res3 = client.post("/api/translate", json={"text": "Давай сократим сроки доставки", "source_field": "en"})
    print("\n3. 'Давай сократим сроки доставки' (RU typed in EN box):")
    print(json.dumps(res3.json(), ensure_ascii=False, indent=2))
    assert res3.status_code == 200
    assert res3.json()["field_corrected"] is True
    assert res3.json()["category"] == "Логистика и ВЭД"

    # 4. Create card with translated content
    trans = res1.json()["translation"]
    cat = res1.json()["category"]
    res4 = client.post("/api/cards", json={
        "user_id": 1,
        "phrase_en": "Keep me in the loop",
        "phrase_ru": trans,
        "category": cat
    })
    print("\n4. Create Card:")
    print(res4.json())
    assert res4.status_code == 200

    print("\n✅ All server tests passed successfully!")

if __name__ == "__main__":
    run_tests()
