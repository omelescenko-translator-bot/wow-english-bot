# -*- coding: utf-8 -*-
"""
Утилита быстрого импорта новых слов и фраз в словарь бота.
Поддерживает:
1. Excel файлы (.xlsx, .xls) со столбцами [Фраза, Перевод]
2. Текстовые файлы (.txt) со строками "Фраза - Перевод" или с разделителем Tab / Запятая
3. Вставку текста прямо в консоль или из буфера
"""

import os
import sys
import openpyxl
from database.db import init_db, add_card, get_stats, get_connection

def import_from_excel(file_path: str, user_id: int = 1):
    if not os.path.exists(file_path):
        print(f"❌ Файл не найден: {file_path}")
        return 0
        
    wb = openpyxl.load_workbook(file_path, data_only=True)
    ws = wb.active
    
    imported = 0
    for row_idx, row in enumerate(ws.iter_rows(values_only=True), 1):
        if row_idx == 1:
            # Check if header
            vals_str = " ".join([str(v or '') for v in row]).lower()
            if 'предложение' in vals_str or 'phrase' in vals_str or 'english' in vals_str:
                continue
                
        # Find EN and RU columns
        non_empty = [str(v).strip() for v in row if v is not None and str(v).strip()]
        if len(non_empty) >= 2:
            # If column 1 is number (1, 2, 3...)
            if non_empty[0].isdigit() and len(non_empty) >= 3:
                en = non_empty[1]
                ru = non_empty[2]
                cat = non_empty[3] if len(non_empty) > 3 else 'Общее'
            else:
                en = non_empty[0]
                ru = non_empty[1]
                cat = non_empty[2] if len(non_empty) > 2 else 'Общее'
                
            if add_card(user_id, en, ru, cat):
                imported += 1
                
    print(f"✅ Успешно импортировано {imported} фраз из Excel: {file_path}")
    return imported

def import_from_text(text: str, user_id: int = 1):
    lines = text.strip().split('\n')
    imported = 0
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
            
        en, ru = '', ''
        if '\t' in line:
            parts = line.split('\t')
            en, ru = parts[0].strip(), parts[1].strip()
        elif ' — ' in line:
            parts = line.split(' — ')
            en, ru = parts[0].strip(), parts[1].strip()
        elif ' - ' in line:
            parts = line.split(' - ')
            en, ru = parts[0].strip(), parts[1].strip()
        elif ':' in line:
            parts = line.split(':')
            en, ru = parts[0].strip(), parts[1].strip()
        else:
            en = line
            ru = ''
            
        if en:
            if add_card(user_id, en, ru):
                imported += 1
                
    print(f"✅ Успешно импортировано {imported} фраз из текста.")
    return imported

if __name__ == '__main__':
    init_db()
    default_excel = os.path.join(os.path.dirname(__file__), 'data', 'my_words.xlsx')
    
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if path.endswith('.xlsx') or path.endswith('.xls'):
            import_from_excel(path)
        else:
            with open(path, 'r', encoding='utf-8') as f:
                import_from_text(f.read())
    else:
        print(f"Импорт из стандартного шаблона: {default_excel}")
        import_from_excel(default_excel)
        
    stats = get_stats(1)
    print(f"\n📊 Текущая статистика словаря:")
    print(f"Всего карточек: {stats['total']}")
    print(f"К повторению сегодня: {stats['to_review']}")
    print(f"Выучено (3+ успешных повторения): {stats['learned']}")
