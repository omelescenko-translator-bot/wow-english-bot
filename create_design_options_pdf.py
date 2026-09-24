# -*- coding: utf-8 -*-
"""
Генератор PDF-презентации вариантов визуализации дизайна WOW English Mini App & Bot
4 пронумерованных варианта (2 тёмных, 2 светлых) с визуальными мокапами и цветовыми палитрами.
"""
import os
import sys
from PIL import Image as PILImage, ImageDraw, ImageFont, ImageFilter
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 1. Register Cyrillic Fonts
font_dir = r'C:\Windows\Fonts'
arial_path = os.path.join(font_dir, 'arial.ttf')
arial_bd_path = os.path.join(font_dir, 'arialbd.ttf')
arial_i_path = os.path.join(font_dir, 'ariali.ttf')

pdfmetrics.registerFont(TTFont('Arial', arial_path))
pdfmetrics.registerFont(TTFont('Arial-Bold', arial_bd_path))
pdfmetrics.registerFont(TTFont('Arial-Italic', arial_i_path))

ARTIFACTS_DIR = r'C:\Users\Admin\.gemini\antigravity-ide\brain\e6538339-685b-4f7c-97cf-d33c6ab55edc'
OUTPUT_DIR = r'c:\PROJECTS\English_Learning_Bot'

# Generate mockups for Concept 3 and Concept 4
def draw_rounded_rect(draw, bounds, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(bounds, radius=radius, fill=fill, outline=outline, width=width)

def create_concept_3_image():
    # Concept 3: Midnight Deep Navy & Emerald Gold (Dark)
    w, h = 720, 1280
    img = PILImage.new('RGBA', (w, h), (13, 21, 39, 255))
    draw = ImageDraw.Draw(img)

    # Ambient radial gradient
    overlay = PILImage.new('RGBA', (w, h), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    ov_draw.ellipse([(-50, -50), (450, 450)], fill=(5, 150, 105, 50))
    ov_draw.ellipse([(350, 700), (850, 1200)], fill=(245, 158, 11, 45))
    overlay = overlay.filter(ImageFilter.GaussianBlur(60))
    img = PILImage.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    try:
        font_large = ImageFont.truetype(arial_bd_path, 42)
        font_med = ImageFont.truetype(arial_bd_path, 26)
        font_sub = ImageFont.truetype(arial_path, 24)
        font_small = ImageFont.truetype(arial_path, 20)
        font_btn = ImageFont.truetype(arial_bd_path, 24)
    except Exception:
        font_large = font_med = font_sub = font_small = font_btn = None

    # Header
    # Avatar
    draw.ellipse([(50, 55), (110, 115)], fill=(16, 185, 129, 255))
    draw.text((70, 68), "OM", fill=(255, 255, 255), font=font_med)
    draw.text((125, 62), "Olga M.", fill=(248, 250, 252), font=font_med)
    draw.text((125, 92), "PRO Learner", fill=(16, 185, 129), font=font_small)

    # Streak badge
    draw_rounded_rect(draw, [(520, 60), (670, 110)], 25, fill=(245, 158, 11, 40), outline=(245, 158, 11, 140), width=2)
    draw.text((545, 70), "🔥 12 дн.", fill=(251, 191, 36), font=font_med)

    # Segmented Control
    draw_rounded_rect(draw, [(50, 160), (670, 225)], 18, fill=(20, 30, 55, 200), outline=(255, 255, 255, 30), width=1)
    draw_rounded_rect(draw, [(54, 164), (256, 221)], 14, fill=(16, 185, 129, 230))
    draw.text((105, 178), "Все (76)", fill=(255, 255, 255), font=font_med)
    draw.text((310, 178), "⏳ Учу (62)", fill=(148, 163, 184), font=font_med)
    draw.text((515, 178), "✅ Знаю (14)", fill=(148, 163, 184), font=font_med)

    # Main 3D Card
    card_bounds = [(50, 270), (670, 830)]
    draw_rounded_rect(draw, card_bounds, 32, fill=(22, 32, 60, 240), outline=(245, 158, 11, 100), width=2)

    # Category Chip
    draw_rounded_rect(draw, [(85, 305), (310, 355)], 14, fill=(245, 158, 11, 35), outline=(245, 158, 11, 100), width=1)
    draw.text((105, 318), "💼 Собеседование", fill=(251, 191, 36), font=font_small)

    # Lang pill + speaker
    draw_rounded_rect(draw, [(460, 305), (575, 355)], 12, fill=(16, 185, 129, 35), outline=(16, 185, 129, 100), width=1)
    draw.text((478, 318), "ENGLISH", fill=(52, 211, 153), font=font_small)
    draw.ellipse([(590, 303), (640, 353)], fill=(16, 185, 129, 60), outline=(16, 185, 129, 160), width=2)
    draw.text((605, 315), "🎧", fill=(255, 255, 255), font=font_small)

    # Phrase Text
    draw.text((85, 430), "What is your greatest", fill=(255, 255, 255), font=font_large)
    draw.text((85, 485), "strength at work?", fill=(255, 255, 255), font=font_large)

    draw.text((85, 590), "В чём ваша самая сильная сторона", fill=(148, 163, 184), font=font_sub)
    draw.text((85, 625), "на рабочем месте?", fill=(148, 163, 184), font=font_sub)

    # Hint
    draw_rounded_rect(draw, [(190, 750), (530, 795)], 20, fill=(13, 21, 39, 180), outline=(255, 255, 255, 20), width=1)
    draw.text((220, 762), "👆 Нажмите, чтобы перевернуть", fill=(100, 116, 139), font=font_small)

    # Action Controls
    # Repeat / Learning
    draw_rounded_rect(draw, [(50, 875), (230, 975)], 22, fill=(245, 158, 11, 35), outline=(245, 158, 11, 140), width=2)
    draw.text((115, 895), "⏳", fill=(251, 191, 36), font=font_med)
    draw.text((95, 930), "Учу", fill=(251, 191, 36), font=font_btn)

    # Flip
    draw_rounded_rect(draw, [(250, 875), (470, 975)], 22, fill=(16, 185, 129, 40), outline=(16, 185, 129, 140), width=2)
    draw.text((345, 895), "🔄", fill=(255, 255, 255), font=font_med)
    draw.text((295, 930), "Перевернуть", fill=(255, 255, 255), font=font_btn)

    # Known
    draw_rounded_rect(draw, [(490, 875), (670, 975)], 22, fill=(16, 185, 129, 200), outline=(52, 211, 153, 220), width=2)
    draw.text((565, 895), "✅", fill=(255, 255, 255), font=font_med)
    draw.text((545, 930), "Знаю", fill=(255, 255, 255), font=font_btn)

    # Bottom Dock Nav
    draw_rounded_rect(draw, [(60, 1150), (660, 1235)], 28, fill=(20, 30, 55, 230), outline=(255, 255, 255, 40), width=1)
    draw.text((130, 1175), "🃏 Карточки", fill=(52, 211, 153), font=font_med)
    draw.text((330, 1175), "📖 Словарь", fill=(148, 163, 184), font=font_med)
    draw.text((515, 1175), "🔥 Прогресс", fill=(148, 163, 184), font=font_med)

    c3_path = os.path.join(ARTIFACTS_DIR, "concept_3_dark_midnight_emerald.png")
    img.save(c3_path, "PNG")
    return c3_path

def create_concept_4_image():
    # Concept 4: Soft Pastel Lavender & Glass Frost (Light)
    w, h = 720, 1280
    img = PILImage.new('RGBA', (w, h), (245, 243, 255, 255))
    draw = ImageDraw.Draw(img)

    # Ambient soft pastel orbs
    overlay = PILImage.new('RGBA', (w, h), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    ov_draw.ellipse([(-40, -40), (450, 450)], fill=(238, 215, 255, 160))
    ov_draw.ellipse([(350, 650), (850, 1150)], fill=(254, 226, 226, 140))
    overlay = overlay.filter(ImageFilter.GaussianBlur(60))
    img = PILImage.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    try:
        font_large = ImageFont.truetype(arial_bd_path, 42)
        font_med = ImageFont.truetype(arial_bd_path, 26)
        font_sub = ImageFont.truetype(arial_path, 24)
        font_small = ImageFont.truetype(arial_path, 20)
        font_btn = ImageFont.truetype(arial_bd_path, 24)
    except Exception:
        font_large = font_med = font_sub = font_small = font_btn = None

    # Header
    draw.ellipse([(50, 55), (110, 115)], fill=(167, 139, 250, 255))
    draw.text((70, 68), "OM", fill=(255, 255, 255), font=font_med)
    draw.text((125, 62), "Olga M.", fill=(30, 27, 75), font=font_med)
    draw.text((125, 92), "Active Learner", fill=(124, 58, 237), font=font_small)

    # Streak badge
    draw_rounded_rect(draw, [(520, 60), (670, 110)], 25, fill=(254, 243, 199, 200), outline=(252, 211, 77, 200), width=2)
    draw.text((545, 70), "🔥 12 дн.", fill=(217, 119, 6), font=font_med)

    # Segmented Control
    draw_rounded_rect(draw, [(50, 160), (670, 225)], 18, fill=(255, 255, 255, 200), outline=(233, 213, 255, 200), width=1)
    draw_rounded_rect(draw, [(54, 164), (256, 221)], 14, fill=(139, 92, 246, 240))
    draw.text((105, 178), "Все (76)", fill=(255, 255, 255), font=font_med)
    draw.text((310, 178), "⏳ Учу (62)", fill=(107, 114, 128), font=font_med)
    draw.text((515, 178), "✅ Знаю (14)", fill=(107, 114, 128), font=font_med)

    # Main Card
    card_bounds = [(50, 270), (670, 830)]
    draw_rounded_rect(draw, card_bounds, 32, fill=(255, 255, 255, 240), outline=(221, 214, 254, 220), width=2)

    # Category Chip
    draw_rounded_rect(draw, [(85, 305), (330, 355)], 14, fill=(243, 232, 255, 240), outline=(216, 180, 254, 180), width=1)
    draw.text((105, 318), "💼 Деловая переписка", fill=(126, 34, 206), font=font_small)

    # Lang pill + speaker
    draw_rounded_rect(draw, [(460, 305), (575, 355)], 12, fill=(236, 253, 245, 240), outline=(167, 243, 208, 200), width=1)
    draw.text((478, 318), "ENGLISH", fill=(5, 150, 105), font=font_small)
    draw.ellipse([(590, 303), (640, 353)], fill=(243, 232, 255, 240), outline=(192, 132, 252, 200), width=2)
    draw.text((605, 315), "🎧", fill=(126, 34, 206), font=font_small)

    # Phrase Text
    draw.text((85, 430), "I look forward to", fill=(30, 27, 75), font=font_large)
    draw.text((85, 485), "hearing from you soon.", fill=(30, 27, 75), font=font_large)

    draw.text((85, 590), "С нетерпением жду вашего ответа", fill=(107, 114, 128), font=font_sub)
    draw.text((85, 625), "в ближайшее время.", fill=(107, 114, 128), font=font_sub)

    # Hint
    draw_rounded_rect(draw, [(190, 750), (530, 795)], 20, fill=(243, 232, 255, 180), outline=(233, 213, 255, 150), width=1)
    draw.text((220, 762), "👆 Нажмите, чтобы перевернуть", fill=(124, 58, 237), font=font_small)

    # Action Controls
    # Repeat / Learning
    draw_rounded_rect(draw, [(50, 875), (230, 975)], 22, fill=(254, 243, 199, 200), outline=(251, 191, 36, 200), width=2)
    draw.text((115, 895), "⏳", fill=(217, 119, 6), font=font_med)
    draw.text((95, 930), "Учу", fill=(217, 119, 6), font=font_btn)

    # Flip
    draw_rounded_rect(draw, [(250, 875), (470, 975)], 22, fill=(243, 232, 255, 220), outline=(192, 132, 252, 220), width=2)
    draw.text((345, 895), "🔄", fill=(109, 40, 217), font=font_med)
    draw.text((295, 930), "Перевернуть", fill=(109, 40, 217), font=font_btn)

    # Known
    draw_rounded_rect(draw, [(490, 875), (670, 975)], 22, fill=(209, 250, 229, 220), outline=(52, 211, 153, 220), width=2)
    draw.text((565, 895), "✅", fill=(5, 150, 105), font=font_med)
    draw.text((545, 930), "Знаю", fill=(5, 150, 105), font=font_btn)

    # Bottom Dock Nav
    draw_rounded_rect(draw, [(60, 1150), (660, 1235)], 28, fill=(255, 255, 255, 230), outline=(233, 213, 255, 200), width=1)
    draw.text((130, 1175), "🃏 Карточки", fill=(124, 58, 237), font=font_med)
    draw.text((330, 1175), "📖 Словарь", fill=(107, 114, 128), font=font_med)
    draw.text((515, 1175), "🔥 Прогресс", fill=(107, 114, 128), font=font_med)

    c4_path = os.path.join(ARTIFACTS_DIR, "concept_4_light_pastel_lavender.png")
    img.save(c4_path, "PNG")
    return c4_path

def build_pdf_presentation():
    c1_path = os.path.join(ARTIFACTS_DIR, "concept_1_dark_cyber_obsidian_1788349742023.jpg")
    c2_path = os.path.join(ARTIFACTS_DIR, "concept_2_light_clean_indigo_1788349759666.jpg")
    c3_path = create_concept_3_image()
    c4_path = create_concept_4_image()

    pdf_file = os.path.join(OUTPUT_DIR, "Design_Themes_Options.pdf")
    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=A4,
        leftMargin=32,
        rightMargin=32,
        topMargin=32,
        bottomMargin=32
    )

    story = []

    # Typography Styles
    title_style = ParagraphStyle(
        'MainTitle',
        fontName='Arial-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0F172A'),
        alignment=0,
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'MainSubTitle',
        fontName='Arial',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#475569'),
        spaceAfter=14
    )
    concept_title = ParagraphStyle(
        'ConceptTitle',
        fontName='Arial-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=4,
        spaceAfter=6
    )
    badge_style = ParagraphStyle(
        'Badge',
        fontName='Arial-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#4F46E5')
    )
    body_p = ParagraphStyle(
        'BodyP',
        fontName='Arial',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#334155'),
        spaceAfter=6
    )
    bullet_p = ParagraphStyle(
        'BulletP',
        fontName='Arial',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#1E293B'),
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3
    )

    # -------------------------------------------------------------
    # PAGE 1: HEADER & CONCEPT 1 (Dark) + CONCEPT 2 (Light)
    # -------------------------------------------------------------
    story.append(Paragraph("🇬🇧 WOW English — Варианты Визуализации Дизайна", title_style))
    story.append(Paragraph("Выберите наиболее комфортный вариант интерфейса для ежедневных занятий. Все варианты оптимизированы под мобильный Telegram Mini App и браузер.", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#E2E8F0'), spaceAfter=14))

    # TABLE 1: CONCEPT 1 vs CONCEPT 2
    # Left: Concept 1, Right: Concept 2
    img_w, img_h = 220, 390

    c1_desc = """
    <b>ВАРИАНТ №1: «Cyber Obsidian & Neon Aurora»</b><br/>
    <font color="#8B5CF6"><b>🌙 ТЁМНАЯ ТЕМА — Футуристичный Неон</b></font><br/><br/>
    • <b>Фон:</b> Глубокий обсидиановый чёрный (<code>#0A0D14</code>) со светящимися аурными сферами Electric Indigo.<br/>
    • <b>Карточка:</b> Матовое стекло с градиентной неоновой окантовкой и мягким неоновым свечением.<br/>
    • <b>Кнопки:</b> Неоновый янтарь (Учу), Индиго (Flip), Изумруд (Знаю).<br/>
    • <b>Атмосфера:</b> Высокотехнологично, стильно, фокус на тексте в темноте.
    """

    c2_desc = """
    <b>ВАРИАНТ №2: «Clean Alabaster & Royal Indigo»</b><br/>
    <font color="#4F46E5"><b>☀️ СВЕТЛАЯ ТЕМА — Скандинавский Apple-минимализм</b></font><br/><br/>
    • <b>Фон:</b> Мягкий матовый фарфоровый белый (<code>#F8FAFD</code>) без слепящего белого света.<br/>
    • <b>Карточка:</b> Парящая белая карточка с мягкой объёмной тенью и глубоким синим индиго (<code>#4F46E5</code>).<br/>
    • <b>Кнопки:</b> Минималистичные круглые пилюли с чёткими иконками.<br/>
    • <b>Атмосфера:</b> Спокойно, легко читается, идеально для дневного времени.
    """

    row1 = [
        Image(c1_path, width=img_w, height=img_h),
        Image(c2_path, width=img_w, height=img_h)
    ]
    row2 = [
        Paragraph(c1_desc, body_p),
        Paragraph(c2_desc, body_p)
    ]

    t1 = Table([row1, row2], colWidths=[265, 265])
    t1.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t1)

    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 2: CONCEPT 3 (Dark) + CONCEPT 4 (Light)
    # -------------------------------------------------------------
    story.append(Paragraph("Варианты визуализации (Продолжение)", title_style))
    story.append(Paragraph("Дополнительные варианты премиального делового и мягкого пастельного стилей:", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#E2E8F0'), spaceAfter=14))

    c3_desc = """
    <b>ВАРИАНТ №3: «Midnight Navy & Emerald Gold»</b><br/>
    <font color="#059669"><b>🌙 ТЁМНАЯ ТЕМА — Премиальный Деловой Сапфир</b></font><br/><br/>
    • <b>Фон:</b> Глубокий благородный ночной сапфир (<code>#0D1527</code>) с тёмно-графитовым стеклом.<br/>
    • <b>Карточка:</b> Элегантная тёмная карточка с золотой каймой (<code>#F59E0B</code>) и изумрудными бейджами.<br/>
    • <b>Кнопки:</b> Золотые и изумрудные акценты, статусный Executive-стиль.<br/>
    • <b>Атмосфера:</b> Престижно, солидно, идеально для бизнес-английского.
    """

    c4_desc = """
    <b>ВАРИАНТ №4: «Soft Pastel Lavender & Frost»</b><br/>
    <font color="#7C3AED"><b>☀️ СВЕТЛАЯ ТЕМА — Мягкая Лаванда и Матовое Стекло</b></font><br/><br/>
    • <b>Фон:</b> Нежный лавандово-персиковый градиентный фон (<code>#F5F3FF</code>) с тёплыми отблесками.<br/>
    • <b>Карточка:</b> Воздушное матовое полупрозрачное стекло с размытием (Glassmorphism).<br/>
    • <b>Кнопки:</b> Мягкие пастельные оттенки (лаванда, мята, нежный персик).<br/>
    • <b>Атмосфера:</b> Уютно, эстетично, расслабляюще и вдохновляюще.
    """

    row3 = [
        Image(c3_path, width=img_w, height=img_h),
        Image(c4_path, width=img_w, height=img_h)
    ]
    row4 = [
        Paragraph(c3_desc, body_p),
        Paragraph(c4_desc, body_p)
    ]

    t2 = Table([row3, row4], colWidths=[265, 265])
    t2.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t2)

    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 3: СРАВНИТЕЛЬНАЯ ТАБЛИЦА И ВЫБОР
    # -------------------------------------------------------------
    story.append(Paragraph("📊 Сводная таблица вариантов дизайна", title_style))
    story.append(Paragraph("Выберите номер варианта, который вам больше всего откликается визуально:", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#E2E8F0'), spaceAfter=14))

    summary_data = [
        [
            Paragraph("<b>№</b>", bullet_p),
            Paragraph("<b>Название концепта</b>", bullet_p),
            Paragraph("<b>Тип темы</b>", bullet_p),
            Paragraph("<b>Ключевая палитра</b>", bullet_p),
            Paragraph("<b>Особенности и настроение</b>", bullet_p)
        ],
        [
            Paragraph("<b>1</b>", bullet_p),
            Paragraph("<b>Cyber Obsidian</b>", bullet_p),
            Paragraph("🌙 Тёмная", bullet_p),
            Paragraph("Obsidian Black, Electric Indigo, Neon Amber & Mint", body_p),
            Paragraph("Футуристичный, неоновые светящиеся кнопки, максимальный контраст текста.", body_p)
        ],
        [
            Paragraph("<b>2</b>", bullet_p),
            Paragraph("<b>Clean Alabaster</b>", bullet_p),
            Paragraph("☀️ Светлая", bullet_p),
            Paragraph("Porcelain White, Royal Indigo, Slate Blue", body_p),
            Paragraph("Скандинавский минимализм (стиль Apple/Linear), чистота и легкость для глаз.", body_p)
        ],
        [
            Paragraph("<b>3</b>", bullet_p),
            Paragraph("<b>Midnight Navy</b>", bullet_p),
            Paragraph("🌙 Тёмная", bullet_p),
            Paragraph("Deep Sapphire, Luxury Emerald, Warm Gold", body_p),
            Paragraph("Премиальный деловой стиль (Duolingo Max / FinTech), золотые и изумрудные бейджи.", body_p)
        ],
        [
            Paragraph("<b>4</b>", bullet_p),
            Paragraph("<b>Pastel Lavender</b>", bullet_p),
            Paragraph("☀️ Светлая", bullet_p),
            Paragraph("Soft Lavender, Peach, Frosted Glass, Lilac", body_p),
            Paragraph("Уютный пастельный глассморфизм, нежные градиенты и мягкие тени.", body_p)
        ]
    ]

    sum_table = Table(summary_data, colWidths=[25, 110, 75, 150, 170])
    sum_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(sum_table)

    story.append(Spacer(1, 20))

    callout_box = [
        [
            Paragraph(
                "💡 <b>Как сделать выбор:</b><br/>"
                "Просто напишите в чат номер варианта: <b>1, 2, 3 или 4</b> (или например: <i>«Мне нравится Вариант 1 для ночи и Вариант 2 для дня»</i>).<br/>"
                "Я сразу активирую и применю выбранный дизайн во всём приложении!",
                body_p
            )
        ]
    ]
    callout_table = Table(callout_box, colWidths=[530])
    callout_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EEF2FF')),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#6366F1')),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
    ]))
    story.append(callout_table)

    doc.build(story)
    print("PDF build successful:", pdf_file)

    # Also copy to root C:\PROJECTS
    import shutil
    root_pdf = r'c:\PROJECTS\WOW_English_Design_Variants.pdf'
    shutil.copyfile(pdf_file, root_pdf)
    print("Copied to root:", root_pdf)

if __name__ == '__main__':
    build_pdf_presentation()
