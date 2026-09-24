import sqlite3

conn = sqlite3.connect('data/vocabulary.db')
cursor = conn.cursor()
cursor.execute("UPDATE cards SET trainer_status = 'neutral' WHERE group_id = 10 AND user_id = 466788167")
cursor.execute("UPDATE study_groups SET status = 'new' WHERE id = 10 AND user_id = 466788167")
conn.commit()
print("Group 10 reset to neutral and status: new")
conn.close()
