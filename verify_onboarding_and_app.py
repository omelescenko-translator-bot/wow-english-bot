# -*- coding: utf-8 -*-
import sys
import os
import requests
import json

try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

BASE_URL = "http://127.0.0.1:8000"

def test_endpoints():
    print("--- 1. Testing Static Assets & Versioning ---")
    r_html = requests.get(f"{BASE_URL}/")
    assert r_html.status_code == 200, f"HTML status: {r_html.status_code}"
    assert "style.css?v=9.4" in r_html.text, "style.css?v=9.4 missing in HTML"
    assert "app.js?v=9.4" in r_html.text, "app.js?v=9.4 missing in HTML"
    assert "onboarding-spotlight-overlay" in r_html.text, "Overlay missing in HTML"
    print("✅ HTML and v=9.4 asset tags verified!")

    r_css = requests.get(f"{BASE_URL}/style.css?v=9.4")
    assert r_css.status_code == 200, f"CSS status: {r_css.status_code}"
    assert "body.onboarding-step-1 .card-scene-container" in r_css.text, "Step 1 card selector missing in CSS"
    assert "body.onboarding-step-2 .dict-top-bar" in r_css.text, "Step 2 top bar selector missing in CSS"
    assert "pulseDockSpotlight" in r_css.text, "pulseDockSpotlight missing in CSS"
    assert "pulseBtnSpotlight" in r_css.text, "pulseBtnSpotlight missing in CSS"
    print("✅ style.css spotlight rules verified!")

    r_js = requests.get(f"{BASE_URL}/app.js?v=9.4")
    assert r_js.status_code == 200, f"JS status: {r_js.status_code}"
    assert "checkAndShowOnboarding" in r_js.text, "checkAndShowOnboarding missing in JS"
    assert "hideOnboardingSpotlight" in r_js.text, "hideOnboardingSpotlight missing in JS"
    print("✅ app.js onboarding functions verified!")

    print("\n--- 2. Testing API & Zero Cards Onboarding State ---")
    # Reset Rozencranz 49367425
    from database.db import get_all_cards, delete_card, get_or_create_user
    user = get_or_create_user(49367425, "Rozencranz", "Rozencranz")
    cards = get_all_cards(49367425, user['native_lang'], user['target_lang'])
    for c in cards:
        delete_card(c['id'], 49367425)

    r_cards = requests.get(f"{BASE_URL}/api/cards?user_id=49367425")
    assert r_cards.status_code == 200, f"API cards status: {r_cards.status_code}"
    cards_data = r_cards.json()
    assert len(cards_data) == 0, f"Expected 0 cards for new user onboarding, got {len(cards_data)}"
    print(f"✅ User 49367425 has 0 cards ({len(cards_data)} cards) -> Clean Onboarding will trigger!")

    print("\n--- 3. Testing Admin Analytics & Export ---")
    r_admin = requests.get(f"{BASE_URL}/api/admin/analytics?user_id=466788167")
    assert r_admin.status_code == 200, f"Admin analytics status: {r_admin.status_code}"
    print(f"✅ Admin analytics verified: total_users={r_admin.json().get('total_users')}")

    r_export = requests.get(f"{BASE_URL}/api/admin/export-excel?user_id=466788167")
    assert r_export.status_code == 200, f"Admin export status: {r_export.status_code}"
    print(f"✅ Admin Excel export verified ({len(r_export.content)} bytes)")

if __name__ == "__main__":
    try:
        test_endpoints()
        print("\n🎉 ALL TESTS PASSED SUCCESSFULLY!")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)
