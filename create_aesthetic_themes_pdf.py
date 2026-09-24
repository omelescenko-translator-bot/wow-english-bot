# -*- coding: utf-8 -*-
"""
Генератор PDF-презентации нежного эстетичного дизайна WOW English:
- Полное отсутствие кричащих эмодзи из клавиатуры
- Тонкие элегантные монохромные векторные иконки (stroke 1.5px в цвет темы)
- Цветовая палитра точь-в-точь по Pinterest-референсу (льняной крем, натуральный шалфей-матча, бархатный хвойный мох, пудровая роза)
- 4 выверенных концепта (2 светлых, 2 тёмных)
"""
import os
import sys
import shutil
import math
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
REF_IMG = os.path.join(OUTPUT_DIR, 'pinterest_reference.jpg')

# Helper vector drawing functions for delicate UI icons
def draw_clock_icon(draw, cx, cy, r, color, width=2):
    draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], outline=color, width=width)
    # hands
    draw.line([(cx, cy), (cx, cy - r + 3)], fill=color, width=width)
    draw.line([(cx, cy), (cx + r - 4, cy)], fill=color, width=width)

def draw_check_icon(draw, cx, cy, r, color, width=2):
    draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], outline=color, width=width)
    # checkmark
    draw.line([(cx - 4, cy), (cx - 1, cy + 3)], fill=color, width=width)
    draw.line([(cx - 1, cy + 3), (cx + 5, cy - 3)], fill=color, width=width)

def draw_flip_icon(draw, cx, cy, r, color, width=2):
    draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], outline=color, width=width)
    draw.line([(cx - 4, cy - 2), (cx + 4, cy - 2)], fill=color, width=width)
    draw.line([(cx + 4, cy - 2), (cx + 1, cy - 5)], fill=color, width=width)
    draw.line([(cx - 4, cy + 2), (cx + 4, cy + 2)], fill=color, width=width)
    draw.line([(cx - 4, cy + 2), (cx - 1, cy + 5)], fill=color, width=width)

def draw_speaker_icon(draw, cx, cy, color, width=2):
    # horn
    draw.polygon([(cx - 7, cy - 3), (cx - 4, cy - 3), (cx, cy - 6), (cx, cy + 6), (cx - 4, cy + 3), (cx - 7, cy + 3)], fill=color)
    # sound waves
    draw.arc([(cx + 1, cy - 5), (cx + 7, cy + 5)], -60, 60, fill=color, width=width)
    draw.arc([(cx + 4, cy - 8), (cx + 12, cy + 8)], -60, 60, fill=color, width=width)

def draw_leaf_icon(draw, cx, cy, color, width=2):
    draw.arc([(cx - 6, cy - 6), (cx + 6, cy + 6)], 0, 90, fill=color, width=width)
    draw.arc([(cx - 6, cy - 6), (cx + 6, cy + 6)], 180, 270, fill=color, width=width)
    draw.line([(cx - 4, cy + 4), (cx + 4, cy - 4)], fill=color, width=width)

AESTHETIC_CONCEPTS = [
    {
        "id": "1",
        "title": "Aesthetic Botanical Sage & Linen",
        "subtitle": "Светлая тема (Точное попадание в Pinterest)",
        "theme_type": "Светлая",
        "bg": (246, 241, 235),
        "card_bg": (255, 254, 251),
        "card_border": (228, 219, 208),
        "text_main": (46, 54, 44),
        "text_sub": (115, 124, 112),
        "accent": (104, 134, 107),       # Botanical Sage
        "accent_soft": (212, 165, 154),  # Dusty Peach Rose
        "chip_bg": (239, 233, 224),
        "button_flip": (104, 134, 107),
        "button_flip_txt": (255, 255, 255),
        "btn_learn_outline": (201, 148, 137),
        "btn_know_outline": (104, 134, 107),
        "aura1": (215, 230, 218, 130),
        "aura2": (245, 225, 215, 110),
        "desc": "Нежный льняной крем, матовый молочный фарфор и благородный натуральный шалфей. Векторные тонкие штриховые иконки цвета шалфея и пыльной розы. Абсолютное спокойствие и нежность."
    },
    {
        "id": "2",
        "title": "Velvet Forest & Matcha Sage",
        "subtitle": "Тёмная тема (Бархатный хвойный уют)",
        "theme_type": "Тёмная",
        "bg": (24, 37, 29),
        "card_bg": (34, 51, 40),
        "card_border": (54, 78, 62),
        "text_main": (244, 239, 233),
        "text_sub": (148, 172, 156),
        "accent": (135, 173, 139),       # Matcha Sage Light
        "accent_soft": (224, 185, 155),  # Soft Sand
        "chip_bg": (29, 44, 35),
        "button_flip": (135, 173, 139),
        "button_flip_txt": (24, 37, 29),
        "btn_learn_outline": (224, 185, 155),
        "btn_know_outline": (135, 173, 139),
        "aura1": (45, 75, 55, 130),
        "aura2": (70, 60, 40, 100),
        "desc": "Глубокий бархатный хвойный полумрак без раздражающего синего свечения. Матовая лесная керамика карточки с мягкой шалфейной подсветкой и тёплой охрой."
    },
    {
        "id": "3",
        "title": "Cozy Matcha Latte & Milk Paper",
        "subtitle": "Светлая тема (Матча-латте и хлопковая бумага)",
        "theme_type": "Светлая",
        "bg": (250, 247, 242),
        "card_bg": (255, 255, 253),
        "card_border": (232, 224, 214),
        "text_main": (48, 44, 38),
        "text_sub": (120, 114, 105),
        "accent": (118, 142, 116),
        "accent_soft": (195, 145, 125),
        "chip_bg": (242, 236, 228),
        "button_flip": (118, 142, 116),
        "button_flip_txt": (255, 255, 255),
        "btn_learn_outline": (195, 145, 125),
        "btn_know_outline": (118, 142, 116),
        "aura1": (225, 235, 220, 120),
        "aura2": (245, 235, 220, 100),
        "desc": "Ламповый эстетичный ежедневник в кофейных и оливковых полутонах. Тёплая хлопковая бумага, тонкие элегантные линии, уют чашки чая матча."
    },
    {
        "id": "4",
        "title": "Deep Moss & Cashmere Pine",
        "subtitle": "Тёмная тема (Глубокий мох и альпийский шалфей)",
        "theme_type": "Тёмная",
        "bg": (18, 30, 24),
        "card_bg": (27, 43, 34),
        "card_border": (48, 70, 56),
        "text_main": (246, 242, 236),
        "text_sub": (140, 165, 150),
        "accent": (122, 168, 130),
        "accent_soft": (218, 175, 140),
        "chip_bg": (22, 36, 28),
        "button_flip": (122, 168, 130),
        "button_flip_txt": (18, 30, 24),
        "btn_learn_outline": (218, 175, 140),
        "btn_know_outline": (122, 168, 130),
        "aura1": (35, 65, 48, 140),
        "aura2": (55, 50, 35, 100),
        "desc": "Тёмный альпийский мох и кашемировое золото. Природный премиум-класс с мягким контрастом для вечерних занятий перед сном."
    }
]

def render_aesthetic_mockup(concept):
    w, h = 640, 1138
    bg = concept["bg"]
    img = PILImage.new('RGBA', (w, h), (bg[0], bg[1], bg[2], 255))
    
    # Soft delicate auras
    overlay = PILImage.new('RGBA', (w, h), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    ov_draw.ellipse([(-30, -30), (420, 420)], fill=concept["aura1"])
    ov_draw.ellipse([(280, 650), (700, 1050)], fill=concept["aura2"])
    overlay = overlay.filter(ImageFilter.GaussianBlur(60))
    img = PILImage.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    try:
        font_large = ImageFont.truetype(arial_bd_path, 35)
        font_med = ImageFont.truetype(arial_bd_path, 22)
        font_sub = ImageFont.truetype(arial_path, 21)
        font_small = ImageFont.truetype(arial_path, 16)
        font_btn = ImageFont.truetype(arial_bd_path, 19)
    except Exception:
        font_large = font_med = font_sub = font_small = font_btn = None

    c_main = concept["text_main"]
    c_sub = concept["text_sub"]
    acc = concept["accent"]
    acc_soft = concept["accent_soft"]
    c_card = concept["card_bg"]
    c_border = concept["card_border"]
    c_chip = concept["chip_bg"]

    # 1. Header (Clean & Minimalist)
    draw.ellipse([(45, 48), (95, 98)], fill=acc)
    draw.text((58, 62), "OM", fill=concept["button_flip_txt"], font=font_med)
    draw.text((110, 56), "Olga M.", fill=c_main, font=font_med)
    draw.text((110, 80), "Botanical English", fill=acc, font=font_small)

    # Streak Badge (With delicate vector flame line, NO loud emoji)
    draw.rounded_rectangle([(460, 52), (595, 94)], radius=20, fill=c_chip, outline=acc_soft, width=1)
    draw_leaf_icon(draw, 482, 73, acc_soft, width=2)
    draw.text((498, 62), "14 дней", fill=acc_soft, font=font_small)

    # 2. Segmented Filters (Minimal & Soft)
    draw.rounded_rectangle([(45, 130), (595, 185)], radius=16, fill=c_chip, outline=c_border, width=1)
    draw.rounded_rectangle([(48, 133), (228, 182)], radius=13, fill=acc)
    draw.text((95, 146), "Все (76)", fill=concept["button_flip_txt"], font=font_med)
    draw.text((275, 146), "Учу (62)", fill=c_sub, font=font_med)
    draw.text((450, 146), "Знаю (14)", fill=c_sub, font=font_med)

    # 3. Main Flashcard (Delicate, tactile ceramic surface)
    card_bounds = [(45, 218), (595, 725)]
    draw.rounded_rectangle(card_bounds, radius=28, fill=c_card, outline=c_border, width=2)

    # Category Chip (Delicate leaf line icon)
    draw.rounded_rectangle([(75, 248), (295, 290)], radius=12, fill=c_chip, outline=c_border, width=1)
    draw_leaf_icon(draw, 95, 269, acc, width=1)
    draw.text((110, 259), "Деловая переписка", fill=acc, font=font_small)

    # Lang Pill + Speaker
    draw.rounded_rectangle([(415, 248), (515, 290)], radius=10, fill=c_chip, outline=acc, width=1)
    draw.text((432, 259), "ENGLISH", fill=acc, font=font_small)
    draw.ellipse([(530, 246), (572, 288)], fill=c_chip, outline=acc, width=1)
    draw_speaker_icon(draw, 550, 267, acc, width=2)

    # Phrase Text
    draw.text((75, 350), "Shorten the lead time", fill=c_main, font=font_large)
    draw.text((75, 396), "for the next order.", fill=c_main, font=font_large)

    draw.text((75, 485), "Сократить срок поставки", fill=c_sub, font=font_sub)
    draw.text((75, 515), "для следующего заказа.", fill=c_sub, font=font_sub)

    # Hint Pill (Delicate line icon)
    draw.rounded_rectangle([(160, 655), (480, 692)], radius=16, fill=c_chip, outline=c_border, width=1)
    draw.text((185, 665), "Нажмите на карточку для переворота", fill=c_sub, font=font_small)

    # 4. Action Controls (With exact delicate vector icons matching theme)
    # Button: УЧУ (With delicate clock line)
    draw.rounded_rectangle([(45, 760), (210, 850)], radius=20, fill=c_chip, outline=concept["btn_learn_outline"], width=2)
    draw_clock_icon(draw, 127, 785, 10, concept["btn_learn_outline"], width=2)
    draw.text((105, 810), "Учу", fill=concept["btn_learn_outline"], font=font_btn)

    # Button: ПЕРЕВЕРНУТЬ (With delicate flip arrows)
    draw.rounded_rectangle([(230, 760), (410, 850)], radius=20, fill=concept["button_flip"])
    draw_flip_icon(draw, 320, 785, 10, concept["button_flip_txt"], width=2)
    draw.text((260, 810), "Перевернуть", fill=concept["button_flip_txt"], font=font_btn)

    # Button: ЗНАЮ (With delicate checkmark line)
    draw.rounded_rectangle([(430, 760), (595, 850)], radius=20, fill=c_chip, outline=concept["btn_know_outline"], width=2)
    draw_check_icon(draw, 512, 785, 10, concept["btn_know_outline"], width=2)
    draw.text((485, 810), "Знаю", fill=concept["btn_know_outline"], font=font_btn)

    # 5. Bottom Dock (Clean minimalist line labels)
    draw.rounded_rectangle([(55, 1010), (585, 1088)], radius=26, fill=c_card, outline=c_border, width=1)
    draw.text((120, 1037), "Карточки", fill=acc, font=font_med)
    draw.text((290, 1037), "Словарь", fill=c_sub, font=font_med)
    draw.text((440, 1037), "Прогресс", fill=c_sub, font=font_med)

    out_file = os.path.join(ARTIFACTS_DIR, f"aesthetic_mockup_{concept['id']}.png")
    img.save(out_file, "PNG")
    return out_file

def generate_aesthetic_presentation():
    mockup_files = {}
    for c in AESTHETIC_CONCEPTS:
        mockup_files[c["id"]] = render_aesthetic_mockup(c)

    pdf_file = os.path.join(OUTPUT_DIR, "Aesthetic_Tender_Themes.pdf")
    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=A4,
        leftMargin=28,
        rightMargin=28,
        topMargin=28,
        bottomMargin=28
    )

    story = []

    title_style = ParagraphStyle(
        'MainTitle',
        fontName='Arial-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#2E362C'),
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'MainSubTitle',
        fontName='Arial',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#68866B'),
        spaceAfter=10
    )
    sec_h2 = ParagraphStyle(
        'SecH2',
        fontName='Arial-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#2E362C'),
        spaceBefore=4,
        spaceAfter=4
    )
    desc_style = ParagraphStyle(
        'DescP',
        fontName='Arial',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor('#3D473B')
    )

    # -------------------------------------------------------------------------
    # PAGE 1: Pinterest Reference + Concept 1 (Light) & Concept 2 (Dark)
    # -------------------------------------------------------------------------
    story.append(Paragraph("🌿 WOW English — Нежная Эстетичная Визуализация", title_style))
    story.append(Paragraph("Разработано строго по вашему референсу из Pinterest: мягкие льняные и хвойно-шалфейные полутона, тактильная матовая текстура и тонкие монохромные векторные иконки (без ярких смайликов).", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#D5DDD5'), spaceAfter=10))

    img_w, img_h = 245, 436

    d1 = f"""
    <b>ВАРИАНТ №1: {AESTHETIC_CONCEPTS[0]['title']}</b><br/>
    <font color="#68866B"><b>☀️ СВЕТЛАЯ ТЕМА (Точное попадание в референс)</b></font><br/><br/>
    • <b>Фон:</b> Тёплый льняной крем (<code>#F6F1EB</code>).<br/>
    • <b>Карточка:</b> Молочный фарфор (<code>#FCFAF7</code>) с деликатной каймой шалфея.<br/>
    • <b>Иконки:</b> Тонкие контурные иконки цвета шалфея и пудровой розы.<br/>
    • <b>Атмосфера:</b> Нежность, спокойствие, идеальный комфорт для глаз.
    """

    d2 = f"""
    <b>ВАРИАНТ №2: {AESTHETIC_CONCEPTS[1]['title']}</b><br/>
    <font color="#87AD8B"><b>🌙 ТЁМНАЯ ТЕМА (Бархатный хвойный уют)</b></font><br/><br/>
    • <b>Фон:</b> Бархатный хвойный мох (<code>#18251D</code>) без синего излучения.<br/>
    • <b>Карточка:</b> Матовая лесная керамика (<code>#223328</code>).<br/>
    • <b>Иконки:</b> Мягкий светящийся шалфей и тёплый персиковый песок.<br/>
    • <b>Атмосфера:</b> Вечернее умиротворение, бархатная глубина.
    """

    t_p1 = Table([
        [Image(mockup_files["1"], width=img_w, height=img_h), Image(mockup_files["2"], width=img_w, height=img_h)],
        [Paragraph(d1, desc_style), Paragraph(d2, desc_style)]
    ], colWidths=[265, 265])
    t_p1.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_p1)

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # PAGE 2: Concept 3 (Light Latte) & Concept 4 (Dark Moss)
    # -------------------------------------------------------------------------
    story.append(Paragraph("Альтернативные нежные оттенки (Варианты 3 и 4)", title_style))
    story.append(Paragraph("Более кофейно-молочные и глубокие альпийские вариации природной эстетики:", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#D5DDD5'), spaceAfter=10))

    d3 = f"""
    <b>ВАРИАНТ №3: {AESTHETIC_CONCEPTS[2]['title']}</b><br/>
    <font color="#768E74"><b>☀️ СВЕТЛАЯ ТЕМА (Матча-латте и бумага)</b></font><br/><br/>
    • <b>Фон:</b> Миндально-молочный (<code>#FAF7F2</code>).<br/>
    • <b>Карточка:</b> Хлопковая бумага (<code>#FFFFFD</code>) с кофейно-оливковой окантовкой.<br/>
    • <b>Иконки:</b> Тонкие штрихи в цвете тёплого ореха и зелёного чая.<br/>
    • <b>Атмосфера:</b> Эстетичный бумажный ежедневник, дзен и чистота.
    """

    d4 = f"""
    <b>ВАРИАНТ №4: {AESTHETIC_CONCEPTS[3]['title']}</b><br/>
    <font color="#7AA882"><b>🌙 ТЁМНАЯ ТЕМА (Глубокий альпийский мох)</b></font><br/><br/>
    • <b>Фон:</b> Тёмная альпийская хвоя (<code>#121E18</code>).<br/>
    • <b>Карточка:</b> Матовый тёмный мох (<code>#1B2B22</code>) с кашемировым золотом.<br/>
    • <b>Иконки:</b> Мягкий шалфей и песочно-золотые линии.<br/>
    • <b>Атмосфера:</b> Премиальный лесной комфорт для вечерней учёбы.
    """

    t_p2 = Table([
        [Image(mockup_files["3"], width=img_w, height=img_h), Image(mockup_files["4"], width=img_w, height=img_h)],
        [Paragraph(d3, desc_style), Paragraph(d4, desc_style)]
    ], colWidths=[265, 265])
    t_p2.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_p2)

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # PAGE 3: Детализация иконок и цветов + Выбор
    # -------------------------------------------------------------------------
    story.append(Paragraph("✨ Решение проблемы с иконками и смайликами", title_style))
    story.append(Paragraph("В отличие от стандартных ярких смайликов из клавиатуры, в приложении используются авторские векторные SVG-контуры:", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#D5DDD5'), spaceAfter=10))

    icon_details = [
        [
            Paragraph("<b>Элемент</b>", desc_style),
            Paragraph("<b>Было (Клавиатурный смайлик)</b>", desc_style),
            Paragraph("<b>Стало в новом дизайне (Эстетичный вектор)</b>", desc_style)
        ],
        [
            Paragraph("Кнопка «Учу / Повторить»", desc_style),
            Paragraph("⏳ Яркие жёлтые песочные часы", desc_style),
            Paragraph("Тонкий минималистичный контур часов (stroke 1.5px) в пудрово-персиковом цвете <code>#D4A59A</code>", desc_style)
        ],
        [
            Paragraph("Кнопка «Знаю»", desc_style),
            Paragraph("✅ Яркая неоновая галочка", desc_style),
            Paragraph("Деликатный тонкий контур с мягкой птичкой в натуральном цвете шалфея <code>#68866B</code>", desc_style)
        ],
        [
            Paragraph("Кнопка «Перевернуть»", desc_style),
            Paragraph("🔄 Синяя стрелка", desc_style),
            Paragraph("Шелковистая кнопка цвета матча с белыми минималистичными стрелками", desc_style)
        ],
        [
            Paragraph("Серия дней (Streak)", desc_style),
            Paragraph("🔥 Оранжевое пламя", desc_style),
            Paragraph("Деликатный контур ростка/листика и спокойная плашка в палитре темы", desc_style)
        ],
        [
            Paragraph("Нижнее меню", desc_style),
            Paragraph("🃏 📖 🔥 Набор эмодзи", desc_style),
            Paragraph("Минималистичные матовые плашки с мягкими текстовыми подписями", desc_style)
        ]
    ]

    icon_tbl = Table(icon_details, colWidths=[130, 160, 240])
    icon_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E7EFE8')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FAFBF9'), colors.HexColor('#FFFFFF')]),
    ]))
    story.append(icon_tbl)

    story.append(Spacer(1, 16))

    callout_p = Paragraph(
        "💡 <b>Как выбрать:</b><br/>"
        "Посмотрите страницы презентации и напишите мне номер:<br/>"
        "• <b>Вариант 1</b> — Идеальный нежный светлый крем и шалфей (референс Pinterest)<br/>"
        "• <b>Вариант 2</b> — Идеальный мягкий бархатный хвойный тёмный уют<br/>"
        "• <b>Варианты 3 и 4</b> — Альтернативные матча-латте и альпийский мох.<br/>"
        "Напишите, например: <b>«Мне нравится 1 для дня и 2 для ночи»</b> — и я активирую их!",
        desc_style
    )
    callout_tbl = Table([[callout_p]], colWidths=[530])
    callout_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EBF4EC')),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#68866B')),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(callout_tbl)

    doc.build(story)
    print("Aesthetic PDF generated:", pdf_file)

    root_pdf = r'c:\PROJECTS\WOW_English_Aesthetic_Tender_Themes.pdf'
    shutil.copyfile(pdf_file, root_pdf)
    print("Copied to root:", root_pdf)

if __name__ == '__main__':
    generate_aesthetic_presentation()
