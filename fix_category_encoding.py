# -*- coding: utf-8 -*-
import sqlite3

conn = sqlite3.connect('data/vocabulary.db')
c = conn.cursor()

cat_logistics = '\u041b\u043e\u0433\u0438\u0441\u0442\u0438\u043a\u0430 \u0438 \u0412\u042d\u0414'
cat_interview = '\u0421\u043e\u0431\u0435\u0441\u0435\u0434\u043e\u0432\u0430\u043d\u0438\u0435'
cat_business = '\u0414\u0435\u043b\u043e\u0432\u0430\u044f \u043f\u0435\u0440\u0435\u043f\u0438\u0441\u043a\u0430'
cat_general = '\u0420\u0430\u0437\u0433\u043e\u0432\u043e\u0440\u043d\u044b\u0439 / \u041e\u0431\u0449\u0435\u0435'

c.execute('SELECT id, phrase_en, phrase_ru FROM cards')
for cid, en, ru in c.fetchall():
    en_l = (en or '').lower()
    ru_l = (ru or '').lower()
    cat = cat_general
    if any(k in en_l for k in ['freight', 'delivery', 'customs', 'shipment', 'stock', 'lead time', 'delayed', 'supply chain', 'invoice', 'order', 'prices']) or any(k in ru_l for k in ['\u0444\u0440\u0430\u0445\u0442', '\u0434\u043e\u0441\u0442\u0430\u0432\u043a', '\u0442\u0430\u043c\u043e\u0436', '\u0441\u043a\u043b\u0430\u0434', '\u043f\u043e\u0441\u0442\u0430\u0432\u043a', '\u0437\u0430\u043a\u0430\u0437', '\u0438\u043d\u0432\u043e\u0439\u0441', '\u0433\u0440\u0443\u0437']):
        cat = cat_logistics
    elif any(k in en_l for k in ['strength', 'weakness', 'hire you', 'current position', 'previous job', 'career development', 'under pressure', 'in a team', 'achievement', 'between the jobs', 'job ad', 'responsible person', 'managed teams', 'involved in']) or any(k in ru_l for k in ['\u0441\u043e\u0431\u0435\u0441\u0435\u0434\u043e\u0432\u0430\u043d', '\u0441\u0438\u043b\u044c\u043d\u0430\u044f \u0441\u0442\u043e\u0440\u043e\u043d\u0430', '\u0441\u043b\u0430\u0431\u044b\u0435 \u0441\u0442\u043e\u0440\u043e\u043d\u044b', '\u043d\u0430\u043d\u044f\u0442\u044c', '\u043a\u0430\u0440\u044c\u0435\u0440\u043d', '\u0440\u0443\u043a\u043e\u0432\u043e\u0434\u0438\u043b', '\u043f\u043e\u0438\u0441\u043a\u0435 \u0440\u0430\u0431\u043e\u0442\u044b']):
        cat = cat_interview
    elif any(k in en_l for k in ['look forward', 'update you', 'keep you posted', 'inconvenience', 'accept their offer', 'access to', 'postpone', 'check these points', 'does that rule']):
        cat = cat_business
    c.execute('UPDATE cards SET category = ? WHERE id = ?', (cat, cid))

c.execute('SELECT id, group_order FROM study_groups')
for gid, order_num in c.fetchall():
    clean_name = f'{order_num} \u0433\u0440\u0443\u043f\u043f\u0430'
    c.execute('UPDATE study_groups SET name = ? WHERE id = ?', (clean_name, gid))

conn.commit()
c.execute('SELECT DISTINCT category FROM cards')
cats = [r[0] for r in c.fetchall()]
conn.close()

with open('scratch_cats.txt', 'w', encoding='utf-8') as f:
    for cat in cats:
        f.write(cat + '\n')
print('Finished updating scratch_cats.txt')
