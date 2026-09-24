# -*- coding: utf-8 -*-
import os
import sys
import requests

try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

BASE_URL = "http://127.0.0.1:8000"

def run_dual_verification():
    print("=" * 60)
    print("🔍 RUNNING DUAL VERIFICATION (User & Admin)")
    print("=" * 60)
    
    # 1. Server Health
    r_health = requests.get(f"{BASE_URL}/health", timeout=3)
    assert r_health.status_code == 200, f"Health check failed: {r_health.status_code}"
    print("✅ 1. Health check: 200 OK")

    # 2. Ordinary User Checks (e.g. Natasha 42001133 or Rozencranz 49367425)
    user_id = 42001133
    r_user_check = requests.get(f"{BASE_URL}/api/admin/check?user_id={user_id}", timeout=3)
    assert r_user_check.status_code == 200
    assert r_user_check.json().get("is_admin") is False, "User should NOT be admin"
    print("✅ 2. Ordinary user role check: is_admin = False (Correct)")

    r_cards = requests.get(f"{BASE_URL}/api/cards?user_id={user_id}", timeout=3)
    assert r_cards.status_code == 200
    print(f"✅ 3. Ordinary user cards API: 200 OK (returned {len(r_cards.json())} cards)")

    r_groups = requests.get(f"{BASE_URL}/api/groups?user_id={user_id}", timeout=3)
    assert r_groups.status_code == 200
    print(f"✅ 4. Ordinary user groups API: 200 OK ({len(r_groups.json())} groups)")

    # Test Non-admin security restriction
    r_non_admin_analytics = requests.get(f"{BASE_URL}/api/admin/analytics?user_id={user_id}", timeout=3)
    assert r_non_admin_analytics.status_code == 403, f"Expected 403 Forbidden, got {r_non_admin_analytics.status_code}"
    print("✅ 5. Security check: Ordinary user forbidden from admin analytics (403 Forbidden)")

    # 3. Administrator Checks (Olga 466788167)
    admin_id = 466788167
    r_admin_check = requests.get(f"{BASE_URL}/api/admin/check?user_id={admin_id}", timeout=3)
    assert r_admin_check.status_code == 200
    assert r_admin_check.json().get("is_admin") is True, "Olga MUST be admin"
    print("✅ 6. Admin role check for Olga (466788167): is_admin = True (Correct)")

    r_admin_cards = requests.get(f"{BASE_URL}/api/cards?user_id={admin_id}", timeout=3)
    assert r_admin_cards.status_code == 200
    print(f"✅ 7. Admin cards API: 200 OK ({len(r_admin_cards.json())} cards for Olga)")

    r_admin_analytics = requests.get(f"{BASE_URL}/api/admin/analytics?user_id={admin_id}", timeout=3)
    assert r_admin_analytics.status_code == 200
    analytics_data = r_admin_analytics.json()
    print(f"✅ 8. Admin analytics API: 200 OK (total_users: {analytics_data.get('total_users')}, total_cards: {analytics_data.get('total_cards')})")

    r_admin_excel = requests.get(f"{BASE_URL}/api/admin/export-excel?user_id={admin_id}", timeout=5)
    assert r_admin_excel.status_code == 200
    assert len(r_admin_excel.content) > 1000
    print(f"✅ 9. Admin Excel export API: 200 OK ({len(r_admin_excel.content)} bytes)")

    # 4. Instant translation check
    r_trans = requests.post(f"{BASE_URL}/api/translate", json={"text": "Привет, как дела?", "source_field": "ru", "native_lang": "ru", "target_lang": "en"}, timeout=5)
    assert r_trans.status_code == 200
    print(f"✅ 10. AI Translation API: 200 OK (Translation: '{r_trans.json().get('translation')}')")

    print("=" * 60)
    print("🎉 ALL DUAL-VERIFICATION TESTS PASSED PERFECTLY!")
    print("=" * 60)

if __name__ == "__main__":
    run_dual_verification()
