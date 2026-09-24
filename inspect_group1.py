import sqlite3, os

conn = sqlite3.connect('data/vocabulary.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute('SELECT id, name, group_order, status FROM study_groups WHERE user_id = 466788167 ORDER BY group_order ASC')
groups = cursor.fetchall()
print('=== GROUPS FOR ADMIN (466788167) ===')
for g in groups:
    cursor.execute('SELECT id, phrase_en, phrase_ru, trainer_status, status FROM cards WHERE group_id = ? ORDER BY id ASC', (g['id'],))
    cards = cursor.fetchall()
    print(f"Group {g['id']} \"{g['name']}\" (order {g['group_order']}) - Status: {g['status']}, Total cards: {len(cards)}")
    for idx, c in enumerate(cards):
        print(f"  [{idx+1}] ID:{c['id']} | {c['phrase_en']} -> {c['phrase_ru']} | trainer_status: {c['trainer_status']}")

conn.close()
