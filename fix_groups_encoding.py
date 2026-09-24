# -*- coding: utf-8 -*-
import sqlite3

conn = sqlite3.connect('data/vocabulary.db')
c = conn.cursor()
c.execute('SELECT id, group_order FROM study_groups')
for gid, order_num in c.fetchall():
    clean_name = f"{order_num} \u0433\u0440\u0443\u043f\u043f\u0430"
    c.execute('UPDATE study_groups SET name = ? WHERE id = ?', (clean_name, gid))
conn.commit()
conn.close()
print("Clean unicode applied.")
