# -*- coding: utf-8 -*-
import os
import json
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from database.db import init_db, import_cards_bulk, get_connection

RAW_DATA = """Предложение	Перевод
Let's meet between Ljubljana and Vienna.	Давай встретимся между Любляной и Веной.
Please write everything in lower case.	Пожалуйста, пишите всё маленькими буквами.
Please start the sentence with a capital letter.	Пожалуйста, начните предложение с заглавной буквы.
Instead of water, I prefer coffee.	Вместо воды я предпочитаю кофе.
I apologize for the inconvenience.	Я извиняюсь за неудобства.
It depends on time.	Это зависит от времени.
The goods will be delivered at your convenience.	Товары будут доставлены, когда вам будет удобно.
Why do I study a lot and earn less?	Почему я много учусь, а зарабатываю меньше?
The client complained.	Клиент пожаловался.
The salary is important to each person.	Зарплата важна для каждого человека.
I look forward to hearing from you.	С нетерпением жду вашего ответа.
We need to compare prices.	Нам нужно сравнить цены.
How much time did it take?	Сколько времени это заняло?
It took me 10 hours.	Это заняло у меня 10 часов.
Can we improve delivery for the next order?	Можем ли мы улучшить доставку для следующего заказа?
Can we find a solution?	Можем ли мы найти решение?
Get used to my hair now.	Привыкай к моим волосам сейчас.
To keep you posted.	Чтобы держать тебя в курсе.
The shipment is stuck at customs clearance.	Груз застрял на таможенном оформлении.
This item is currently out of stock.	Этой позиции сейчас нет на складе.
We need to shorten the lead time.	Нам нужно сократить срок выполнения/поставки.
Delivery is delayed.	Доставка задерживается.
Will it be convenient for you?	Будет ли это удобно для вас?
This is urgent.	Это срочно.
Sea freight, Railway freight, Road freight, Air freight.	Морской фрахт, ж/д фрахт, автодоставка, авиафрахт.
freight rate	Тарифная ставка на перевозку (стоимость фрахта).
Deal with problems.	Разбираться с проблемами.
I can deal with problems on my own.	Я могу разбираться с проблемами самостоятельно.
I need to deal with this invoice first.	Мне нужно сначала разобраться с этим инвойсом.
I'll set it up.	Я всё организую / устрою / настрою.
Honestly	Честно говоря / честно.
Actually	На самом деле / вообще-то.
It depends on many things.	Это зависит от многих вещей.
From time to time.	Время от времени.
I'm confused.	Я в замешательстве / запуталась.
we are going to accept their offer	Мы собираемся принять их предложение
to accept a job offer	принять предложение о работе
give me an access to...	Предоставьте мне доступ к...
only he has an access to the programm	Только у него есть доступ к программе
she was very successful at her job	Она успешна на своей работе
what is Peter repairing?	Что Питер чинит?
Are you ready yet	Ты уже готов?
I think my English is improving slowly	Я думаю, мой английский улучшается медленно
What do you do in your spare time?	Что вы делаете в свободное время?
I am writing to update you on the project	Я пишу, чтобы ввести вас в курс дела по проекту
This job ad has expired	Вакансия закрыта
What is your greatest strength?	В чем ваша сильная сторона?
What are your weaknesses?	Какие ваши слабые стороны?
What has disappointed you about your job?	Что вас разочаровало в вашей работе?
What has been your biggest achievement at work?	Каким было самое большое ваше достижение?
Why are you leaving your current position?	Почему вы покидаете ваше текущее место работы?
What would make you stay at your previous job?	Что могло бы заставить вас остаться на предыдущей работе?
Why should we hire you?	Почему нам стоит вас нанять?
What are you looking for in terms of career development?	К чему вы стремитесь с точки зрения карьерного роста?
I'm not fully satisfied with the work I'm doing	Я не полностью удовлетворен той работой, которую выполняю.
I have an ability to work under pressure	У меня есть способность работы под давлением
I am rather good at working in a team	Я довольно хорошо умею работать в команде
In my most recent job, I was involved in training the staff	На своей предыдущей работе я участвовала в обучении персонала
In my most recent job, I was involved in managment of branch office.	На своей предыдущей работе я участвовала в управлении филиалом.
I consider myself a responsible person.	Я считаю себя ответственным человеком
From start to finish	От начала до конца
Do you mind I open the window?	Вы не против, если я открою окно?
I'm really into yoga	Я очень увлекаюсь йогой
improved	улучшенный
meet / reach goals	достигать целей
I'm between the jobs	Я сейчас в поиске работы
I have several years of experience in supply chain management.	У меня есть несколько лет опыта работы в сфере управления цепочками поставок.
I have managed teams of up to 10 staff.	Я руководил командами численностью ДО 10 человек.
a few things came up	Возникли некоторые обстоятельства
urgent delivery	Срочная доставка
He replied me	Он ответил мне
Does that rule still apply	Эти договоренности ещё действительны?
Please check these points and let me know	Пожалуйста проверьте эти пункты/моменты и дайте знать
product range	Продуктовая линейка
postpone a meeting	Перенести встречу
school principal	Директор школы"""

def categorize(en: str, ru: str) -> str:
    en_l = en.lower()
    ru_l = ru.lower()
    
    # Logistics / Supply Chain
    if any(k in en_l for k in ['freight', 'delivery', 'customs', 'shipment', 'stock', 'lead time', 'delayed', 'supply chain', 'invoice', 'order', 'prices']):
        return 'Логистика и ВЭД'
    if any(k in ru_l for k in ['фрахт', 'доставк', 'тамож', 'склад', 'поставк', 'заказ', 'инвойс', 'груз']):
        return 'Логистика и ВЭД'
        
    # Job Interview
    if any(k in en_l for k in ['strength', 'weakness', 'hire you', 'current position', 'previous job', 'career development', 'under pressure', 'in a team', 'achievement', 'between the jobs', 'job ad', 'responsible person', 'managed teams', 'involved in']):
        return 'Собеседование'
    if any(k in ru_l for k in ['собеседован', 'сильная сторона', 'слабые стороны', 'нанять', 'карьерн', 'руководил', 'поиске работы']):
        return 'Собеседование'
        
    # Business Correspondence
    if any(k in en_l for k in ['look forward', 'update you', 'keep you posted', 'inconvenience', 'accept their offer', 'access to', 'postpone', 'check these points', 'does that rule']):
        return 'Деловая переписка'
        
    return 'Разговорный / Общее'

def build_data():
    init_db()
    
    lines = RAW_DATA.strip().split('\n')
    cards_list = []
    
    for line in lines[1:]:
        parts = line.split('\t')
        en = parts[0].strip() if len(parts) > 0 else ''
        ru = parts[1].strip() if len(parts) > 1 else ''
        if not en and not ru:
            continue
        
        # Handle cases where Russian was in English column (e.g. school principal)
        if any(c in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя' for c in en.lower()) and not any(c in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя' for c in ru.lower()) and ru:
            en, ru = ru, en
            
        cat = categorize(en, ru)
        cards_list.append((en, ru, cat))
        
    print(f'Total cards loaded: {len(cards_list)}')
    
    # Save to JSON
    json_path = os.path.join(os.path.dirname(__file__), 'data', 'initial_phrases.json')
    data_dicts = [{'phrase_en': c[0], 'phrase_ru': c[1], 'category': c[2]} for c in cards_list]
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data_dicts, f, ensure_ascii=False, indent=2)
    print('Saved to JSON:', json_path)
    
    # Create Beautiful Excel Template
    xlsx_path = os.path.join(os.path.dirname(__file__), 'data', 'my_words.xlsx')
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Мой словарь"
    ws.views.sheetView[0].showGridLines = True
    
    # Styling
    header_fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
    header_font = Font(name="Arial", size=11, bold=True, color="FFFFFF")
    row_font = Font(name="Arial", size=10)
    border_thin = Side(border_style="thin", color="E2E8F0")
    border = Border(left=border_thin, right=border_thin, top=border_thin, bottom=border_thin)
    
    headers = ["№", "Фраза на английском (English)", "Перевод на русский", "Категория"]
    ws.append(headers)
    
    for col_num in range(1, 5):
        cell = ws.cell(row=1, column=col_num)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = border
        
    for idx, (en, ru, cat) in enumerate(cards_list, 1):
        row_num = idx + 1
        ws.cell(row=row_num, column=1, value=idx).alignment = Alignment(horizontal="center")
        ws.cell(row=row_num, column=2, value=en)
        ws.cell(row=row_num, column=3, value=ru)
        ws.cell(row=row_num, column=4, value=cat).alignment = Alignment(horizontal="center")
        
        # Zebra striping
        if idx % 2 == 0:
            fill = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
            for c in range(1, 5):
                ws.cell(row=row_num, column=c).fill = fill
                
        for c in range(1, 5):
            ws.cell(row=row_num, column=c).font = row_font
            ws.cell(row=row_num, column=c).border = border
            
    ws.column_dimensions['A'].width = 6
    ws.column_dimensions['B'].width = 50
    ws.column_dimensions['C'].width = 50
    ws.column_dimensions['D'].width = 24
    
    wb.save(xlsx_path)
    print('Excel workbook created at:', xlsx_path)
    
    # Import into master user_id = 1 (default user)
    import_cards_bulk(1, cards_list)
    print('Imported into default user database (ID: 1)')

if __name__ == '__main__':
    build_data()
