# -*- coding: utf-8 -*-
"""
Генератор расширенной PDF-презентации: 10 вариантов уютного дизайна WOW English:
- 5 Светлых вариантов (тёплые бежевые, льняные, овсяные, карамельные, персиковые тона)
- 5 Тёмных вариантов (уютные зелено-синие, глубокий тил, хвойные, изумрудные, океанические тона)
"""
import os
import sys
import shutil
from PIL import Image as PILImage, ImageDraw, ImageFont, ImageFilter
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

font_dir = r'C:\Windows\Fonts'
arial_path = os.path.join(font_dir, 'arial.ttf')
arial_bd_path = os.path.join(font_dir, 'arialbd.ttf')
arial_i_path = os.path.join(font_dir, 'ariali.ttf')

pdfmetrics.registerFont(TTFont('Arial', arial_path))
pdfmetrics.registerFont(TTFont('Arial-Bold', arial_bd_path))
pdfmetrics.registerFont(TTFont('Arial-Italic', arial_i_path))

ARTIFACTS_DIR = r'C:\Users\Admin\.gemini\antigravity-ide\brain\e6538339-685b-4f7c-97cf-d33c6ab55edc'
OUTPUT_DIR = r'c:\PROJECTS\English_Learning_Bot'

THEMES_DEF = [
    # 5 LIGHT THEMES
    {
        "num": 1,
        "name": "Warm Linen & Cozy Sand",
        "type": "Светлая (Льняной беж)",
        "bg_color": (247, 244, 238),
        "card_bg": (255, 253, 249),
        "card_border": (224, 216, 203),
        "text_main": (55, 48, 42),
        "text_sub": (120, 110, 100),
        "accent": (140, 109, 88),      # Warm mocha
        "accent_green": (91, 130, 102),# Sage
        "accent_amber": (212, 143, 56),# Warm Amber
        "chip_bg": (238, 232, 222),
        "aura1": (235, 220, 200, 140),
        "aura2": (220, 230, 220, 120),
        "desc": "Натуральный лён, тёплый песок и мягкий кофейный мокко. Атмосфера спокойной кофейни с книгой."
    },
    {
        "num": 2,
        "name": "Cashmere Sage & Oatmeal",
        "type": "Светлая (Овсянка и Шалфей)",
        "bg_color": (245, 243, 237),
        "card_bg": (254, 253, 250),
        "card_border": (216, 222, 214),
        "text_main": (44, 53, 49),
        "text_sub": (105, 117, 111),
        "accent": (96, 123, 114),      # Sage Green
        "accent_green": (68, 140, 110),
        "accent_amber": (209, 148, 62),
        "chip_bg": (232, 238, 233),
        "aura1": (210, 230, 220, 140),
        "aura2": (240, 230, 210, 120),
        "desc": "Эко-минимализм в тонах овсяного молока и кашемирового шалфея. Снимает напряжение с глаз."
    },
    {
        "num": 3,
        "name": "Warm Latte & Caramel Biscuit",
        "type": "Светлая (Латте и Карамель)",
        "bg_color": (250, 246, 240),
        "card_bg": (255, 255, 253),
        "card_border": (232, 222, 200),
        "text_main": (60, 42, 30),
        "text_sub": (130, 110, 95),
        "accent": (160, 105, 60),      # Caramel
        "accent_green": (80, 135, 95),
        "accent_amber": (225, 150, 45),
        "chip_bg": (243, 233, 218),
        "aura1": (245, 225, 195, 150),
        "aura2": (250, 240, 225, 130),
        "desc": "Мягкие сливочные оттенки латте и песочного бисквита. Ламповый домашний уют и теплота."
    },
    {
        "num": 4,
        "name": "Soft Peach Clay & Cream",
        "type": "Светлая (Персиковая глина)",
        "bg_color": (250, 242, 236),
        "card_bg": (255, 253, 251),
        "card_border": (235, 215, 202),
        "text_main": (65, 45, 40),
        "text_sub": (135, 108, 100),
        "accent": (217, 119, 98),      # Terracotta peach
        "accent_green": (106, 166, 145),
        "accent_amber": (230, 145, 60),
        "chip_bg": (246, 228, 220),
        "aura1": (255, 225, 215, 150),
        "aura2": (240, 235, 215, 120),
        "desc": "Нежная персиковая глина и мягкий крем. Очень деликатные тёплые пастельные тона."
    },
    {
        "num": 5,
        "name": "Honey Butter & Vanilla Mist",
        "type": "Светлая (Мёд и Ваниль)",
        "bg_color": (253, 251, 247),
        "card_bg": (255, 255, 255),
        "card_border": (232, 224, 210),
        "text_main": (48, 50, 54),
        "text_sub": (115, 118, 122),
        "accent": (218, 155, 75),      # Honey Gold
        "accent_green": (75, 150, 115),
        "accent_amber": (225, 140, 40),
        "chip_bg": (248, 239, 220),
        "aura1": (255, 240, 205, 150),
        "aura2": (235, 245, 235, 120),
        "desc": "Воздушная ваниль и тёплый цветочный мёд. Солнечное утро, лёгкость и идеальный контраст."
    },

    # 5 DARK THEMES (GREEN-BLUE / TEAL / EMERALD)
    {
        "num": 6,
        "name": "Nordic Teal & Deep Moss",
        "type": "Тёмная (Северный Тил и Мох)",
        "bg_color": (12, 22, 24),
        "card_bg": (18, 35, 38),
        "card_border": (38, 70, 75),
        "text_main": (240, 248, 248),
        "text_sub": (130, 165, 168),
        "accent": (78, 205, 196),      # Mint Teal
        "accent_green": (78, 205, 196),
        "accent_amber": (245, 166, 35),
        "chip_bg": (24, 48, 52),
        "aura1": (30, 80, 85, 120),
        "aura2": (15, 50, 60, 100),
        "desc": "Глубокий ночной сине-зелёный океан и северный тил. Уютная бархатная глубина без синего свечения."
    },
    {
        "num": 7,
        "name": "Emerald Forest & Warm Amber",
        "type": "Тёмная (Хвойный Изумруд)",
        "bg_color": (11, 26, 23),
        "card_bg": (17, 40, 35),
        "card_border": (35, 80, 70),
        "text_main": (242, 249, 245),
        "text_sub": (135, 170, 158),
        "accent": (82, 183, 136),      # Emerald
        "accent_green": (82, 183, 136),
        "accent_amber": (229, 169, 60),
        "chip_bg": (25, 55, 48),
        "aura1": (25, 90, 70, 130),
        "aura2": (50, 80, 40, 100),
        "desc": "Тёмно-хвойный лесной уют с тёплыми янтарными огоньками. Ощущение вечернего шале у камина."
    },
    {
        "num": 8,
        "name": "Midnight Ocean & Seafoam",
        "type": "Тёмная (Полуночный Океан)",
        "bg_color": (10, 25, 38),
        "card_bg": (16, 38, 56),
        "card_border": (35, 75, 105),
        "text_main": (240, 247, 252),
        "text_sub": (130, 162, 188),
        "accent": (56, 178, 172),      # Aquamarine
        "accent_green": (56, 178, 172),
        "accent_amber": (246, 173, 85),
        "chip_bg": (22, 50, 72),
        "aura1": (20, 75, 110, 130),
        "aura2": (30, 95, 95, 110),
        "desc": "Глубокая полуночная морская вода и матовое стекло цвета морской пены. Кристальное спокойствие."
    },
    {
        "num": 9,
        "name": "Alpine Pine & Cashmere Gold",
        "type": "Тёмная (Альпийская Пихта и Золото)",
        "bg_color": (14, 29, 25),
        "card_bg": (22, 45, 39),
        "card_border": (45, 90, 78),
        "text_main": (245, 248, 244),
        "text_sub": (140, 175, 162),
        "accent": (212, 175, 55),      # Soft Gold
        "accent_green": (116, 198, 157),
        "accent_amber": (212, 175, 55),
        "chip_bg": (30, 60, 52),
        "aura1": (35, 95, 80, 120),
        "aura2": (60, 85, 45, 100),
        "desc": "Премиальная тёмная альпийская пихта с благородным мягким золотом. Природный комфорт высшего класса."
    },
    {
        "num": 10,
        "name": "Deep Cyan Night & Mint Glow",
        "type": "Тёмная (Глубокий Циан и Мята)",
        "bg_color": (8, 23, 30),
        "card_bg": (14, 38, 48),
        "card_border": (30, 78, 96),
        "text_main": (240, 250, 252),
        "text_sub": (125, 168, 180),
        "accent": (100, 223, 223),     # Mint Glow
        "accent_green": (100, 223, 223),
        "accent_amber": (255, 209, 102),
        "chip_bg": (20, 52, 65),
        "aura1": (20, 85, 105, 130),
        "aura2": (15, 60, 75, 110),
        "desc": "Бархатный тёмно-сине-бирюзовый фон с мягким мятным свечением. Максимальный фокус без усталости."
    }
]

def render_theme_mockup(theme_info):
    w, h = 600, 1066
    bg = theme_info["bg_color"]
    img = PILImage.new('RGBA', (w, h), (bg[0], bg[1], bg[2], 255))
    
    # Ambient Auras
    overlay = PILImage.new('RGBA', (w, h), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    ov_draw.ellipse([(-30, -30), (380, 380)], fill=theme_info["aura1"])
    ov_draw.ellipse([(280, 600), (680, 1000)], fill=theme_info["aura2"])
    overlay = overlay.filter(ImageFilter.GaussianBlur(50))
    img = PILImage.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    try:
        font_large = ImageFont.truetype(arial_bd_path, 34)
        font_med = ImageFont.truetype(arial_bd_path, 22)
        font_sub = ImageFont.truetype(arial_path, 20)
        font_small = ImageFont.truetype(arial_path, 16)
        font_btn = ImageFont.truetype(arial_bd_path, 18)
    except Exception:
        font_large = font_med = font_sub = font_small = font_btn = None

    c_main = theme_info["text_main"]
    c_sub = theme_info["text_sub"]
    acc = theme_info["accent"]
    c_green = theme_info["accent_green"]
    c_amber = theme_info["accent_amber"]

    # 1. Header
    draw.ellipse([(40, 45), (90, 95)], fill=acc)
    draw.text((54, 57), "OM", fill=(255, 255, 255), font=font_med)
    draw.text((105, 52), "Olga M.", fill=c_main, font=font_med)
    draw.text((105, 76), "WOW English Learner", fill=acc, font=font_small)

    # Streak badge
    draw.rounded_rectangle([(440, 50), (560, 90)], radius=20, fill=theme_info["chip_bg"], outline=acc, width=1)
    draw.text((460, 58), "🔥 14 дн.", fill=c_amber, font=font_med)

    # 2. Segmented Filters
    draw.rounded_rectangle([(40, 125), (560, 180)], radius=16, fill=theme_info["chip_bg"], outline=theme_info["card_border"], width=1)
    draw.rounded_rectangle([(43, 128), (210, 177)], radius=13, fill=acc)
    draw.text((85, 140), "Все (76)", fill=(255, 255, 255), font=font_med)
    draw.text((255, 140), "⏳ Учу (62)", fill=c_sub, font=font_med)
    draw.text((420, 140), "✅ Знаю (14)", fill=c_sub, font=font_med)

    # 3. Main Flashcard
    card_bounds = [(40, 215), (560, 685)]
    draw.rounded_rectangle(card_bounds, radius=26, fill=theme_info["card_bg"], outline=theme_info["card_border"], width=2)

    # Category Chip
    draw.rounded_rectangle([(65, 240), (280, 280)], radius=12, fill=theme_info["chip_bg"], outline=theme_info["card_border"], width=1)
    draw.text((80, 250), "💼 Деловая переписка", fill=acc, font=font_small)

    # Lang Pill + Speaker
    draw.rounded_rectangle([(390, 240), (485, 280)], radius=10, fill=theme_info["chip_bg"], outline=c_green, width=1)
    draw.text((405, 250), "ENGLISH", fill=c_green, font=font_small)
    draw.ellipse([(500, 238), (540, 278)], fill=theme_info["chip_bg"], outline=acc, width=1)
    draw.text((512, 248), "🎧", fill=acc, font=font_small)

    # Phrase Text
    draw.text((65, 340), "Shorten the lead time", fill=c_main, font=font_large)
    draw.text((65, 385), "for the next order.", fill=c_main, font=font_large)

    draw.text((65, 470), "Сократить срок поставки", fill=c_sub, font=font_sub)
    draw.text((65, 498), "для следующего заказа.", fill=c_sub, font=font_sub)

    # Hint
    draw.rounded_rectangle([(145, 620), (455, 655)], radius=16, fill=theme_info["chip_bg"], outline=theme_info["card_border"], width=1)
    draw.text((165, 630), "👆 Нажмите, чтобы перевернуть", fill=c_sub, font=font_small)

    # 4. Action Buttons
    # Repeat / Learning
    draw.rounded_rectangle([(40, 720), (195, 805)], radius=18, fill=theme_info["chip_bg"], outline=c_amber, width=2)
    draw.text((105, 735), "⏳", fill=c_amber, font=font_med)
    draw.text((90, 765), "Учу", fill=c_amber, font=font_btn)

    # Flip
    draw.rounded_rectangle([(215, 720), (385, 805)], radius=18, fill=acc)
    draw.text((290, 735), "🔄", fill=(255, 255, 255), font=font_med)
    draw.text((250, 765), "Перевернуть", fill=(255, 255, 255), font=font_btn)

    # Known
    draw.rounded_rectangle([(405, 720), (560, 805)], radius=18, fill=theme_info["chip_bg"], outline=c_green, width=2)
    draw.text((470, 735), "✅", fill=c_green, font=font_med)
    draw.text((455, 765), "Знаю", fill=c_green, font=font_btn)

    # 5. Bottom Dock Navigation
    draw.rounded_rectangle([(50, 950), (550, 1025)], radius=24, fill=theme_info["card_bg"], outline=theme_info["card_border"], width=1)
    draw.text((105, 975), "🃏 Карточки", fill=acc, font=font_med)
    draw.text((275, 975), "📖 Словарь", fill=c_sub, font=font_med)
    draw.text((425, 975), "🔥 Прогресс", fill=c_sub, font=font_med)

    out_file = os.path.join(ARTIFACTS_DIR, f"cozy_theme_option_{theme_info['num']}.png")
    img.save(out_file, "PNG")
    return out_file

def generate_full_pdf():
    # 1. Render all 10 mockups
    mockup_paths = {}
    for t in THEMES_DEF:
        p = render_theme_mockup(t)
        mockup_paths[t["num"]] = p

    pdf_file = os.path.join(OUTPUT_DIR, "Cozy_Themes_10_Variants.pdf")
    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=A4,
        leftMargin=28,
        rightMargin=28,
        topMargin=28,
        bottomMargin=28
    )

    story = []

    # Typography Styles
    title_style = ParagraphStyle(
        'MainTitle',
        fontName='Arial-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#1E293B'),
        alignment=0,
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'MainSubTitle',
        fontName='Arial',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#475569'),
        spaceAfter=10
    )
    section_h2 = ParagraphStyle(
        'SecH2',
        fontName='Arial-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=6,
        spaceAfter=4
    )
    card_title = ParagraphStyle(
        'CardTitle',
        fontName='Arial-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#0F172A')
    )
    card_desc = ParagraphStyle(
        'CardDesc',
        fontName='Arial',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#334155')
    )

    img_w, img_h = 160, 284

    # -------------------------------------------------------------------------
    # PAGE 1: COVER & LIGHT THEMES (1, 2)
    # -------------------------------------------------------------------------
    story.append(Paragraph("🇬🇧 WOW English — 10 Вариантов Уютного Дизайна", title_style))
    story.append(Paragraph("Специальная подборка в мягких бежево-пастельных (для дня) и зелено-сине-хвойных тонах (для вечера/ночи). Все варианты созданы для максимального комфорта глаз и уюта.", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=10))

    story.append(Paragraph("☀️ СВЕТЛЫЕ ТЕМЫ: ТЁПЛЫЙ БЕЖ, ЛЁН И ПАСТЕЛЬ", section_h2))

    # Row with Theme 1 and Theme 2
    t1 = THEMES_DEF[0]
    t2 = THEMES_DEF[1]

    d1 = f"<b>ВАРИАНТ №1: {t1['name']}</b><br/><font color='#8C6D58'><b>{t1['type']}</b></font><br/>{t1['desc']}"
    d2 = f"<b>ВАРИАНТ №2: {t2['name']}</b><br/><font color='#607B72'><b>{t2['type']}</b></font><br/>{t2['desc']}"

    row_imgs = [Image(mockup_paths[1], width=img_w, height=img_h), Image(mockup_paths[2], width=img_w, height=img_h)]
    row_texts = [Paragraph(d1, card_desc), Paragraph(d2, card_desc)]

    tbl_p1 = Table([row_imgs, row_texts], colWidths=[265, 265])
    tbl_p1.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(tbl_p1)

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # PAGE 2: LIGHT THEMES (3, 4, 5)
    # -------------------------------------------------------------------------
    story.append(Paragraph("☀️ Светлые темы (Продолжение: 3, 4, 5)", section_h2))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=8))

    img_w3, img_h3 = 165, 290
    t3 = THEMES_DEF[2]
    t4 = THEMES_DEF[3]
    t5 = THEMES_DEF[4]

    d3 = f"<b>ВАРИАНТ №3: {t3['name']}</b><br/><font color='#A0693C'><b>{t3['type']}</b></font><br/>{t3['desc']}"
    d4 = f"<b>ВАРИАНТ №4: {t4['name']}</b><br/><font color='#D97762'><b>{t4['type']}</b></font><br/>{t4['desc']}"
    d5 = f"<b>ВАРИАНТ №5: {t5['name']}</b><br/><font color='#DA9B4B'><b>{t5['type']}</b></font><br/>{t5['desc']}"

    row_imgs_p2 = [
        Image(mockup_paths[3], width=img_w, height=img_h),
        Image(mockup_paths[4], width=img_w, height=img_h)
    ]
    row_texts_p2 = [Paragraph(d3, card_desc), Paragraph(d4, card_desc)]

    tbl_p2 = Table([row_imgs_p2, row_texts_p2], colWidths=[265, 265])
    tbl_p2.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(tbl_p2)

    story.append(Spacer(1, 10))

    # Option 5 Single Row
    tbl_p2_single = Table([
        [Image(mockup_paths[5], width=140, height=248), Paragraph(d5 + "<br/><br/>• <b>Особенность:</b> Нежный солнечный утренний свет, максимальная мягкость бежевых оттенков и высокая читаемость.", card_desc)]
    ], colWidths=[155, 375])
    tbl_p2_single.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(tbl_p2_single)

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # PAGE 3: DARK THEMES (6, 7) — GREEN-BLUE & TEAL
    # -------------------------------------------------------------------------
    story.append(Paragraph("🌙 ТЁМНЫЕ ТЕМЫ: ЗЕЛЕНО-СИНИЕ, ТИЛ И ХВОЯ", section_h2))
    story.append(Paragraph("Мягкая природная тёмная палитра без раздражающего синего излучения и резких контрастов:", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=10))

    t6 = THEMES_DEF[5]
    t7 = THEMES_DEF[6]

    d6 = f"<b>ВАРИАНТ №6: {t6['name']}</b><br/><font color='#4ECDC4'><b>{t6['type']}</b></font><br/>{t6['desc']}"
    d7 = f"<b>ВАРИАНТ №7: {t7['name']}</b><br/><font color='#52B788'><b>{t7['type']}</b></font><br/>{t7['desc']}"

    row_imgs_p3 = [Image(mockup_paths[6], width=img_w, height=img_h), Image(mockup_paths[7], width=img_w, height=img_h)]
    row_texts_p3 = [Paragraph(d6, card_desc), Paragraph(d7, card_desc)]

    tbl_p3 = Table([row_imgs_p3, row_texts_p3], colWidths=[265, 265])
    tbl_p3.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(tbl_p3)

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # PAGE 4: DARK THEMES (8, 9, 10)
    # -------------------------------------------------------------------------
    story.append(Paragraph("🌙 Тёмные темы (Продолжение: 8, 9, 10)", section_h2))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=8))

    t8 = THEMES_DEF[7]
    t9 = THEMES_DEF[8]
    t10 = THEMES_DEF[9]

    d8 = f"<b>ВАРИАНТ №8: {t8['name']}</b><br/><font color='#38B2AC'><b>{t8['type']}</b></font><br/>{t8['desc']}"
    d9 = f"<b>ВАРИАНТ №9: {t9['name']}</b><br/><font color='#74C69D'><b>{t9['type']}</b></font><br/>{t9['desc']}"
    d10 = f"<b>ВАРИАНТ №10: {t10['name']}</b><br/><font color='#64DFDF'><b>{t10['type']}</b></font><br/>{t10['desc']}"

    row_imgs_p4 = [
        Image(mockup_paths[8], width=img_w, height=img_h),
        Image(mockup_paths[9], width=img_w, height=img_h)
    ]
    row_texts_p4 = [Paragraph(d8, card_desc), Paragraph(d9, card_desc)]

    tbl_p4 = Table([row_imgs_p4, row_texts_p4], colWidths=[265, 265])
    tbl_p4.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(tbl_p4)

    story.append(Spacer(1, 10))

    # Option 10 Single Row
    tbl_p4_single = Table([
        [Image(mockup_paths[10], width=140, height=248), Paragraph(d10 + "<br/><br/>• <b>Особенность:</b> Глубокий бархатный циановый ночной фон с мягкой мятой. Очень стильный, современный и комфортный для ночных занятий.", card_desc)]
    ], colWidths=[155, 375])
    tbl_p4_single.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(tbl_p4_single)

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # PAGE 5: СРАВНИТЕЛЬНАЯ ТАБЛИЦА ВСЕХ 10 ВАРИАНТОВ
    # -------------------------------------------------------------------------
    story.append(Paragraph("📊 Сводная таблица всех 10 вариантов", title_style))
    story.append(Paragraph("Выберите номера вариантов (например: №1 для дня и №7 для вечера):", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=10))

    tbl_data = [
        [
            Paragraph("<b>№</b>", card_desc),
            Paragraph("<b>Название концепта</b>", card_desc),
            Paragraph("<b>Тип темы</b>", card_desc),
            Paragraph("<b>Основные цвета</b>", card_desc),
            Paragraph("<b>Атмосфера и уют</b>", card_desc)
        ]
    ]

    for t in THEMES_DEF:
        tbl_data.append([
            Paragraph(f"<b>{t['num']}</b>", card_desc),
            Paragraph(f"<b>{t['name']}</b>", card_desc),
            Paragraph(f"{'☀️' if t['num'] <= 5 else '🌙'} {t['type'].split('(')[0].strip()}", card_desc),
            Paragraph(f"{t['type'].split('(')[1].replace(')', '') if '(' in t['type'] else ''}", card_desc),
            Paragraph(t['desc'], card_desc)
        ])

    summary_tbl = Table(tbl_data, colWidths=[20, 125, 75, 110, 200])
    summary_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,5), [colors.HexColor('#FAFAF7'), colors.HexColor('#FFFFFF')]),
        ('ROWBACKGROUNDS', (0,6), (-1,10), [colors.HexColor('#F0F7F6'), colors.HexColor('#F5FAF9')]),
    ]))
    story.append(summary_tbl)

    story.append(Spacer(1, 16))

    callout_p = Paragraph(
        "💡 <b>Как выбрать:</b><br/>"
        "Напишите мне номер понравившегося варианта (или пару номеров, например: <b>«Мне нравится №1 (или №2) для светлой темы и №7 (или №8) для тёмной»</b>) — и я моментально настрою эти точные оттенки в вашем боте и приложении!",
        card_desc
    )
    callout_tbl = Table([[callout_p]], colWidths=[530])
    callout_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EEF2FF')),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#4F46E5')),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(callout_tbl)

    doc.build(story)
    print("Cozy 10 Themes PDF built successfully:", pdf_file)

    root_pdf = r'c:\PROJECTS\WOW_English_Cozy_Themes_10_Variants.pdf'
    shutil.copyfile(pdf_file, root_pdf)
    print("Copied to root:", root_pdf)

if __name__ == '__main__':
    generate_full_pdf()
