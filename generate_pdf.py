# -*- coding: utf-8 -*-
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register Cyrillic Fonts
pdfmetrics.registerFont(TTFont('Arial', r'C:\Windows\Fonts\arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', r'C:\Windows\Fonts\arialbd.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Italic', r'C:\Windows\Fonts\ariali.ttf'))
pdfmetrics.registerFont(TTFont('Arial-BoldItalic', r'C:\Windows\Fonts\arialbi.ttf'))

pdf_path = r'c:\PROJECTS\English_Learning_Bot\English_Learning_Bot_Concept.pdf'
doc = SimpleDocTemplate(
    pdf_path,
    pagesize=A4,
    leftMargin=36,
    rightMargin=36,
    topMargin=36,
    bottomMargin=36
)

# Custom colors
primary_color = colors.HexColor('#1E293B')   # Slate 800
accent_color = colors.HexColor('#4F46E5')    # Indigo 600
accent_light = colors.HexColor('#EEF2FF')    # Indigo 50
text_dark = colors.HexColor('#0F172A')       # Slate 900
text_muted = colors.HexColor('#475569')      # Slate 600
bg_light = colors.HexColor('#F8FAFC')        # Slate 50
border_color = colors.HexColor('#CBD5E1')    # Slate 300

title_style = ParagraphStyle(
    'DocTitle',
    fontName='Arial-Bold',
    fontSize=18,
    leading=22,
    textColor=primary_color,
    alignment=0,
    spaceAfter=4
)

h1_style = ParagraphStyle(
    'SectionH1',
    fontName='Arial-Bold',
    fontSize=13,
    leading=17,
    textColor=accent_color,
    spaceBefore=8,
    spaceAfter=5
)

h2_style = ParagraphStyle(
    'SectionH2',
    fontName='Arial-Bold',
    fontSize=10.5,
    leading=14.5,
    textColor=primary_color,
    spaceBefore=4,
    spaceAfter=3
)

body_style = ParagraphStyle(
    'BodyDark',
    fontName='Arial',
    fontSize=9,
    leading=13,
    textColor=text_dark,
    spaceAfter=3
)

body_bold = ParagraphStyle(
    'BodyDarkBold',
    fontName='Arial-Bold',
    fontSize=9,
    leading=13,
    textColor=text_dark
)

callout_style = ParagraphStyle(
    'CalloutText',
    fontName='Arial',
    fontSize=8.5,
    leading=12.5,
    textColor=primary_color
)

bullet_style = ParagraphStyle(
    'BulletText',
    fontName='Arial',
    fontSize=8.5,
    leading=12.5,
    textColor=text_dark,
    leftIndent=10,
    firstLineIndent=-6,
    spaceAfter=3
)

story = []

# --- HEADER BANNER ---
header_data = [
    [
        Paragraph('<b>ENGLISH LEARNING BOT & MINI APP</b>', title_style),
        Paragraph('<b>КОНЦЕПЦИЯ И АРХИТЕКТУРА</b><br/><font color="#64748B">Сентябрь 2026 | Версия 1.0</font>', ParagraphStyle('RHead', fontName='Arial', fontSize=9, leading=12, alignment=2, textColor=text_muted))
    ]
]
header_table = Table(header_data, colWidths=[330, 193])
header_table.setStyle(TableStyle([
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ('TOPPADDING', (0,0), (-1,-1), 0),
    ('LEFTPADDING', (0,0), (-1,-1), 0),
    ('RIGHTPADDING', (0,0), (-1,-1), 0),
]))
story.append(header_table)
story.append(Spacer(1, 4))
story.append(HRFlowable(width='100%', thickness=1.5, color=accent_color, spaceBefore=2, spaceAfter=8))

# --- INTRO CALLOUT ---
intro_p = Paragraph(
    '<b>Краткое резюме проекта:</b> Интеллектуальный Telegram-бот нового поколения, объединяющий разговорную практику с AI (текст + голосовые сообщения), автоматический сбор персонального словаря из пересылаемых сообщений и современный интерактивный интерфейс <b>Telegram Mini App (WebApp)</b> для тренировки карточек со свайпами.',
    callout_style
)
intro_table = Table([[intro_p]], colWidths=[523])
intro_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), accent_light),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#C7D2FE')),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
]))
story.append(intro_table)
story.append(Spacer(1, 6))

# --- VISUAL MOCKUP & INTERFACE SECTION ---
story.append(Paragraph('1. Визуальный концепт интерфейса (Telegram Mini App)', h1_style))

img_path = r'c:\PROJECTS\English_Learning_Bot\telegram_miniapp_mockup.jpg'
mockup_img = Image(img_path, width=200, height=255)

ui_desc = [
    Paragraph('<b>Как устроен интерфейс приложения:</b>', h2_style),
    Paragraph('• <b>Плавное открытие:</b> Приложение открывается прямо внутри Telegram нажатием кнопки меню <i>[ 📱 Открыть словарь ]</i> поверх диалога без перехода в браузер.', bullet_style),
    Paragraph('• <b>Интерактивные карточки:</b> Карточки со словами и фразами поддерживают свайпы влево/вправо («Знаю» / «Повторить»), транскрипцию и воспроизведение озвучки.', bullet_style),
    Paragraph('• <b>Геймификация и стрик:</b> В шапке отображается прогресс (серия дней подряд 🔥, уровень B1/B2, количество освоенных фраз).', bullet_style),
    Paragraph('• <b>Контекстные примеры:</b> Каждая фраза сопровождается живым примером употребления в реальной речи.', bullet_style),
    Paragraph('• <b>Нижняя панель навигации:</b> Быстрый переход между разделами: <i>Словарь, Диалог AI, Тесты, Собеседование</i>.', bullet_style),
    Paragraph('• <b>Быстрое закрытие (✖):</b> Мгновенный возврат в чат для общения голосом и текстом.', bullet_style),
]

mockup_table_data = [
    [mockup_img, ui_desc]
]
mockup_table = Table(mockup_table_data, colWidths=[205, 318])
mockup_table.setStyle(TableStyle([
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('LEFTPADDING', (0,0), (-1,-1), 4),
    ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ('TOPPADDING', (0,0), (-1,-1), 2),
    ('BOTTOMPADDING', (0,0), (-1,-1), 2),
]))
story.append(mockup_table)

story.append(PageBreak())

# --- PAGE 2: FUNCTIONAL MODULES ---
story.append(Paragraph('2. Ключевые функциональные модули', h1_style))
story.append(HRFlowable(width='100%', thickness=1, color=border_color, spaceBefore=2, spaceAfter=6))

# Module 1: Vocabulary & Forwarding
mod1_title = Paragraph('<b>📥 Модуль 1: Умный словарь и карточки (Spaced Repetition)</b>', h2_style)
mod1_desc = Paragraph(
    '<b>Механика добавления через пересылку сообщений (Forwarding):</b><br/>'
    'Пользователь пересылает боту любое сообщение из Telegram-каналов, чатов или просто отправляет фразу/слово на английском с переводом или без него.<br/>'
    '• <b>AI-парсинг:</b> Бот мгновенно анализирует текст, выделяет ключевую фразу/слово, определяет контекст и правильный перевод.<br/>'
    '• <b>Автодополнение:</b> Бот автоматически генерирует транскрипцию, пример использования в реальной речи и озвучку.<br/>'
    '• <b>Алгоритм интервальных повторений:</b> Слова распределяются по системе Лейтнера (повтор через 1 день, 3 дня, 7 дней, 21 день) для гарантированного перехода в долговременную память.',
    body_style
)
mod1_table = Table([[mod1_title], [mod1_desc]], colWidths=[523])
mod1_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), bg_light),
    ('BOX', (0,0), (-1,-1), 1, border_color),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
]))
story.append(mod1_table)
story.append(Spacer(1, 6))

# Module 2: Speaking & Voice Trainer
mod2_title = Paragraph('<b>🗣️ Модуль 2: Разговорный AI-тренажёр (Speaking & Voice Practice)</b>', h2_style)
mod2_desc = Paragraph(
    '<b>Практика живой речи с мягкой ненавязчивой коррекцией:</b><br/>'
    '• <b>Голосовой и текстовый режим:</b> Пользователь общается как текстом, так и голосовыми сообщениями (Voice Notes). Бот транскрибирует аудио и отвечает натуральной речью.<br/>'
    '• <b>Мягкое исправление ошибок (Gentle Feedback):</b> Бот не прерывает диалог сухими замечаниями, а органично поддерживает беседу, добавляя в конце короткий аккуратный блок:<br/>'
    '&nbsp;&nbsp;&nbsp;&nbsp;<i>💡 Tip: Вместо "I am agree" естественнее сказать "I agree". Отличная мысль!</i><br/>'
    '• <b>Сценарии и свободные темы:</b> Путешествия, заказ в ресторане, бытовые диалоги, хобби, обсуждение новостей или свободное общение.',
    body_style
)
mod2_table = Table([[mod2_title], [mod2_desc]], colWidths=[523])
mod2_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), bg_light),
    ('BOX', (0,0), (-1,-1), 1, border_color),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
]))
story.append(mod2_table)
story.append(Spacer(1, 6))

# Module 3: Job Interview Preparation
mod3_title = Paragraph('<b>💼 Модуль 3: Подготовка к собеседованиям (Job Interview Prep)</b>', h2_style)
mod3_desc = Paragraph(
    '<b>Симуляция реального интервью на английском языке:</b><br/>'
    '• <b>Выбор роли:</b> Логистика/ВЭД, бэк-офис координатор, аналитик, закупки, менеджер проектов или общие вопросы HR.<br/>'
    '• <b>Пошаговые раунды:</b> Бот задаёт классические и поведенческие вопросы (Self-presentation, Why this company?, Tell about a conflict situation).<br/>'
    '• <b>Методика STAR:</b> Бот помогает структурировать ответы (Situation → Task → Action → Result).<br/>'
    '• <b>Оценка и рекомендации:</b> Анализ профессиональной лексики, уверенности формулировок и предложение более сильных синонимов.',
    body_style
)
mod3_table = Table([[mod3_title], [mod3_desc]], colWidths=[523])
mod3_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), bg_light),
    ('BOX', (0,0), (-1,-1), 1, border_color),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
]))
story.append(mod3_table)

# --- PAGE 3: ARCHITECTURE & ROADMAP ---
story.append(PageBreak())

story.append(Paragraph('3. Архитектура системы и Стек технологий', h1_style))
story.append(HRFlowable(width='100%', thickness=1, color=border_color, spaceBefore=2, spaceAfter=6))

tech_data = [
    [Paragraph('<b>Компонент</b>', body_bold), Paragraph('<b>Технология</b>', body_bold), Paragraph('<b>Назначение</b>', body_bold)],
    [Paragraph('Telegram Backend', body_style), Paragraph('Python + aiogram 3.x', body_style), Paragraph('Быстрый асинхронный бот, обработка команд, пересылок и аудио', body_style)],
    [Paragraph('AI Engine & NLP', body_style), Paragraph('Gemini API (Interactions)', body_style), Paragraph('Анализ фраз, диалоги, мягкая коррекция, симуляция интервью', body_style)],
    [Paragraph('Голосовой модуль', body_style), Paragraph('Gemini / Whisper + TTS', body_style), Paragraph('Распознавание голосовых сообщений и озвучка фраз', body_style)],
    [Paragraph('Mini App Frontend', body_style), Paragraph('HTML5, Modern CSS, JS', body_style), Paragraph('Интерфейс карточек со свайпами внутри Telegram WebApp SDK', body_style)],
    [Paragraph('База данных', body_style), Paragraph('SQLite / PostgreSQL', body_style), Paragraph('Хранение профилей, персональных словарей и дат повторений', body_style)],
]
tech_table = Table(tech_data, colWidths=[120, 130, 273])
tech_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
    ('GRID', (0,0), (-1,-1), 0.5, border_color),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
]))
story.append(tech_table)
story.append(Spacer(1, 10))

story.append(Paragraph('4. Пошаговый план разработки (Roadmap)', h1_style))
story.append(HRFlowable(width='100%', thickness=1, color=border_color, spaceBefore=2, spaceAfter=6))

steps_data = [
    [Paragraph('<b>Этап 1: Ядро бота и Словарь</b>', body_bold), Paragraph('Создание каркаса бота, базы данных пользователей и обработчика пересылки фраз/сообщений с авто-переводом и разбором через AI.', body_style)],
    [Paragraph('<b>Этап 2: Telegram Mini App</b>', body_bold), Paragraph('Разработка веб-интерфейса карточек слов со свайпами («Знаю» / «Повторить»), транскрипцией и синхронизацией с базой бота.', body_style)],
    [Paragraph('<b>Этап 3: Разговорный AI-тренажёр</b>', body_bold), Paragraph('Подключение текстового и голосового диалога с мягкой ненавязчивой коррекцией грамматики и подсказками.', body_style)],
    [Paragraph('<b>Этап 4: Симулятор собеседований</b>', body_bold), Paragraph('Модуль отработки интервью по ролям и методике STAR с разбором ответов и рекомендациями.', body_style)],
    [Paragraph('<b>Этап 5: Тестирование и запуск</b>', body_bold), Paragraph('Комплексная проверка всех сценариев, тестирование в Telegram.', body_style)],
]
steps_table = Table(steps_data, colWidths=[160, 363])
steps_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), bg_light),
    ('GRID', (0,0), (-1,-1), 0.5, border_color),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('RIGHTPADDING', (0,0), (-1,-1), 8),
]))
story.append(steps_table)

doc.build(story)
print('PDF created successfully at:', pdf_path)
