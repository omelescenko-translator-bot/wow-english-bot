# -*- coding: utf-8 -*-
"""
Генератор PDF-визуализации стиля «Тактильное дерево и мягкая глина» (Neumorphic Warm Wood & Soft Clay)
по новому референсу пользователя:
- Светлое дерево / скандинавский бук и глина (Warm Birch Wood & Cream Clay)
- Тёмный мощёный дуб / орех (Smoked Walnut & Dark Clay)
- Эффект мягкого 3D-барельефа и гравировки (Neumorphism / Soft Embossed / Carved)
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

def draw_neumorphic_card(img, bounds, bg_col, shadow_dark, shadow_light, radius=32):
    """Рисует мягкую выпуклую 3D-плитку с эффектом мягкого дерева/глины"""
    w, h = img.size
    x1, y1 = bounds[0]
    x2, y2 = bounds[1]
    
    # Layer 1: Dark soft drop shadow (bottom-right)
    shadow_dark_img = PILImage.new('RGBA', (w, h), (0, 0, 0, 0))
    d1 = ImageDraw.Draw(shadow_dark_img)
    d1.rounded_rectangle([(x1 + 10, y1 + 10), (x2 + 10, y2 + 10)], radius=radius, fill=shadow_dark)
    shadow_dark_img = shadow_dark_img.filter(ImageFilter.GaussianBlur(14))
    img = PILImage.alpha_composite(img, shadow_dark_img)

    # Layer 2: Light soft highlight (top-left)
    shadow_light_img = PILImage.new('RGBA', (w, h), (0, 0, 0, 0))
    d2 = ImageDraw.Draw(shadow_light_img)
    d2.rounded_rectangle([(x1 - 8, y1 - 8), (x2 - 8, y2 - 8)], radius=radius, fill=shadow_light)
    shadow_light_img = shadow_light_img.filter(ImageFilter.GaussianBlur(12))
    img = PILImage.alpha_composite(img, shadow_light_img)

    # Layer 3: Main surface
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(bounds, radius=radius, fill=bg_col)
    
    # Bevel top highlight line
    draw.rounded_rectangle([(x1+1, y1+1), (x2-1, y2-1)], radius=radius-1, outline=(255, 255, 255, 120) if bg_col[0] > 100 else (60, 50, 42, 100), width=1)
    
    return img

def draw_debossed_panel(img, bounds, bg_col, shadow_dark, shadow_light, radius=20):
    """Рисует вдавленную панель (инсет / выемка в дереве)"""
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(bounds, radius=radius, fill=bg_col)
    x1, y1 = bounds[0]
    x2, y2 = bounds[1]
    # Inner shadow simulation (top & left dark, bottom & right light)
    draw.line([(x1+radius, y1+1), (x2-radius, y1+1)], fill=shadow_dark, width=2)
    draw.line([(x1+1, y1+radius), (x1+1, y2-radius)], fill=shadow_dark, width=2)
    draw.line([(x1+radius, y2-1), (x2-radius, y2-1)], fill=shadow_light, width=2)
    draw.line([(x2-1, y1+radius), (x2-1, y2-radius)], fill=shadow_light, width=2)
    return img

WOOD_THEMES = [
    {
        "id": "1",
        "title": "Scandinavian Birch & Warm Clay",
        "subtitle": "Светлая тема (Светлое дерево / бук / тёплая глина)",
        "theme_type": "Светлая",
        "bg_col": (239, 232, 222, 255),
        "card_bg": (239, 232, 222, 255),
        "shadow_dark": (180, 164, 148, 180),
        "shadow_light": (255, 255, 255, 240),
        "inset_bg": (228, 220, 208, 255),
        "text_main": (68, 55, 45),        # Deep Warm Walnut
        "text_sub": (135, 120, 108),      # Muted Sand Taupe
        "accent": (168, 120, 85),         # Warm Terracotta Teak
        "accent_green": (102, 133, 106),  # Sage Leaf
        "accent_warm": (195, 130, 95),    # Clay Peach
        "btn_flip_bg": (178, 135, 100, 255),
        "btn_flip_txt": (255, 255, 255),
        "desc": "Тактильное мягкое светлое дерево и тёплая глина. Объёмные выпуклые карточки и выдавленные деревянные кнопки с мягкими тенями. Абсолютный скандинавский уют."
    },
    {
        "id": "2",
        "title": "Smoked Walnut & Charcoal Wood",
        "subtitle": "Тёмная тема (Мореный тёмный дуб / орех)",
        "theme_type": "Тёмная",
        "bg_col": (32, 27, 23, 255),
        "card_bg": (38, 32, 28, 255),
        "shadow_dark": (12, 10, 8, 220),
        "shadow_light": (60, 52, 45, 160),
        "inset_bg": (26, 22, 19, 255),
        "text_main": (244, 234, 224),     # Warm Cream
        "text_sub": (155, 142, 130),      # Sand Dust
        "accent": (218, 162, 108),        # Amber Honey Wood
        "accent_green": (138, 175, 140),  # Forest Moss
        "accent_warm": (225, 155, 115),   # Terracotta Ember
        "btn_flip_bg": (195, 142, 92, 255),
        "btn_flip_txt": (32, 27, 23),
        "desc": "Глубокое мореное тёмное дерево, орех и обожжённая глина. Мягкий объёмный барельеф для вечерней учёбы, тёплый янтарный свет камина."
    },
    {
        "id": "3",
        "title": "Honey Oak & Natural Linen",
        "subtitle": "Светлая тема (Медовый дуб и натуральный лён)",
        "theme_type": "Светлая",
        "bg_col": (245, 239, 230, 255),
        "card_bg": (245, 239, 230, 255),
        "shadow_dark": (190, 175, 160, 160),
        "shadow_light": (255, 255, 255, 230),
        "inset_bg": (235, 227, 216, 255),
        "text_main": (60, 48, 38),
        "text_sub": (128, 112, 98),
        "accent": (185, 130, 78),         # Honey Amber
        "accent_green": (95, 130, 100),
        "accent_warm": (205, 140, 95),
        "btn_flip_bg": (185, 130, 78, 255),
        "btn_flip_txt": (255, 255, 255),
        "desc": "Тёплый медовый дуб, льняные текстуры и мягкий тактильный рельеф. Очень светлый, согревающий домашний дизайн."
    },
    {
        "id": "4",
        "title": "Nordic Pine & Forest Moss",
        "subtitle": "Тёмная тема (Северная сосна и мох)",
        "theme_type": "Тёмная",
        "bg_col": (26, 32, 28, 255),
        "card_bg": (32, 40, 35, 255),
        "shadow_dark": (10, 15, 12, 220),
        "shadow_light": (50, 62, 55, 160),
        "inset_bg": (20, 26, 22, 255),
        "text_main": (240, 245, 240),
        "text_sub": (145, 165, 150),
        "accent": (125, 178, 135),        # Sage Pine
        "accent_green": (125, 178, 135),
        "accent_warm": (220, 165, 110),
        "btn_flip_bg": (105, 155, 115, 255),
        "btn_flip_txt": (20, 28, 22),
        "desc": "Тёмное хвойное дерево северной сосны с моховым барельефом. Максимально расслабляющее погружение для вечернего обучения."
    }
]

def render_wood_mockup(theme):
    w, h = 640, 1138
    bg = theme["bg_col"]
    img = PILImage.new('RGBA', (w, h), bg)
    
    # 1. Background subtle wood grain / light auras
    overlay = PILImage.new('RGBA', (w, h), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    ov_draw.ellipse([(-30, -30), (450, 450)], fill=(theme["shadow_light"][0], theme["shadow_light"][1], theme["shadow_light"][2], 40))
    ov_draw.ellipse([(250, 650), (700, 1100)], fill=(theme["shadow_dark"][0], theme["shadow_dark"][1], theme["shadow_dark"][2], 30))
    overlay = overlay.filter(ImageFilter.GaussianBlur(50))
    img = PILImage.alpha_composite(img, overlay)

    try:
        font_large = ImageFont.truetype(arial_bd_path, 35)
        font_med = ImageFont.truetype(arial_bd_path, 22)
        font_sub = ImageFont.truetype(arial_path, 21)
        font_small = ImageFont.truetype(arial_path, 16)
        font_btn = ImageFont.truetype(arial_bd_path, 19)
    except Exception:
        font_large = font_med = font_sub = font_small = font_btn = None

    c_main = theme["text_main"]
    c_sub = theme["text_sub"]
    acc = theme["accent"]
    acc_green = theme["accent_green"]
    acc_warm = theme["accent_warm"]

    # 2. Header (Neumorphic Profile Button & Streak Pill)
    # Profile avatar
    img = draw_neumorphic_card(img, [(45, 48), (100, 103)], theme["card_bg"], theme["shadow_dark"], theme["shadow_light"], radius=18)
    draw = ImageDraw.Draw(img)
    draw.text((61, 64), "OM", fill=acc, font=font_med)
    draw.text((115, 58), "Olga M.", fill=c_main, font=font_med)
    draw.text((115, 82), "Wood & Clay Edition", fill=acc, font=font_small)

    # Streak pill (Carved inset)
    img = draw_debossed_panel(img, [(465, 52), (595, 96)], theme["inset_bg"], theme["shadow_dark"], theme["shadow_light"], radius=18)
    draw = ImageDraw.Draw(img)
    draw.text((485, 64), "🌿 14 дней", fill=acc_warm, font=font_small)

    # 3. Segmented Filter (Debossed Wood Channel + Raised Active Wood Button)
    img = draw_debossed_panel(img, [(45, 130), (595, 185)], theme["inset_bg"], theme["shadow_dark"], theme["shadow_light"], radius=18)
    # Active pill (Raised 3D tile)
    img = draw_neumorphic_card(img, [(48, 133), (228, 182)], theme["card_bg"], theme["shadow_dark"], theme["shadow_light"], radius=15)
    draw = ImageDraw.Draw(img)
    draw.text((95, 146), "Все (76)", fill=acc, font=font_med)
    draw.text((275, 146), "Учу (62)", fill=c_sub, font=font_med)
    draw.text((450, 146), "Знаю (14)", fill=c_sub, font=font_med)

    # 4. Main Flashcard (Giant 3D Raised Soft Wood Tile with Beveled Rim)
    card_bounds = [(45, 218), (595, 725)]
    img = draw_neumorphic_card(img, card_bounds, theme["card_bg"], theme["shadow_dark"], theme["shadow_light"], radius=36)
    draw = ImageDraw.Draw(img)

    # Category Chip (Engraved Inset)
    img = draw_debossed_panel(img, [(75, 248), (295, 290)], theme["inset_bg"], theme["shadow_dark"], theme["shadow_light"], radius=14)
    draw = ImageDraw.Draw(img)
    draw.text((95, 259), "Деловая переписка", fill=acc, font=font_small)

    # Speaker Button (3D Raised circular Wood Knob)
    img = draw_neumorphic_card(img, [(525, 245), (570, 290)], theme["card_bg"], theme["shadow_dark"], theme["shadow_light"], radius=22)
    draw = ImageDraw.Draw(img)
    # Speaker icon
    cx, cy = 547, 267
    draw.polygon([(cx - 7, cy - 3), (cx - 4, cy - 3), (cx, cy - 6), (cx, cy + 6), (cx - 4, cy + 3), (cx - 7, cy + 3)], fill=acc)
    draw.arc([(cx + 1, cy - 5), (cx + 7, cy + 5)], -60, 60, fill=acc, width=2)

    # Phrase Text (Carved look)
    draw.text((75, 350), "Shorten the lead time", fill=c_main, font=font_large)
    draw.text((75, 396), "for the next order.", fill=c_main, font=font_large)

    draw.text((75, 485), "Сократить срок поставки", fill=c_sub, font=font_sub)
    draw.text((75, 515), "для следующего заказа.", fill=c_sub, font=font_sub)

    # Hint Inset
    img = draw_debossed_panel(img, [(145, 655), (495, 692)], theme["inset_bg"], theme["shadow_dark"], theme["shadow_light"], radius=16)
    draw = ImageDraw.Draw(img)
    draw.text((168, 665), "Нажмите на карточку для переворота", fill=c_sub, font=font_small)

    # 5. Action Controls (3D Tactile Wood & Clay Buttons)
    # Repeat / Learning (Soft 3D Carved)
    img = draw_neumorphic_card(img, [(45, 760), (210, 850)], theme["card_bg"], theme["shadow_dark"], theme["shadow_light"], radius=24)
    draw = ImageDraw.Draw(img)
    # Clock line icon
    cx, cy = 127, 785
    draw.ellipse([(cx - 10, cy - 10), (cx + 10, cy + 10)], outline=acc_warm, width=2)
    draw.line([(cx, cy), (cx, cy - 7)], fill=acc_warm, width=2)
    draw.line([(cx, cy), (cx + 6, cy)], fill=acc_warm, width=2)
    draw.text((105, 810), "Учу", fill=acc_warm, font=font_btn)

    # Flip Button (Raised Accent Wood / Clay)
    img = draw_neumorphic_card(img, [(230, 760), (410, 850)], theme["btn_flip_bg"], theme["shadow_dark"], theme["shadow_light"], radius=24)
    draw = ImageDraw.Draw(img)
    # Flip arrows
    cx, cy = 320, 785
    draw.line([(cx - 7, cy - 2), (cx + 7, cy - 2)], fill=theme["btn_flip_txt"], width=2)
    draw.line([(cx + 7, cy - 2), (cx + 3, cy - 6)], fill=theme["btn_flip_txt"], width=2)
    draw.line([(cx - 7, cy + 2), (cx + 7, cy + 2)], fill=theme["btn_flip_txt"], width=2)
    draw.line([(cx - 7, cy + 2), (cx - 3, cy + 6)], fill=theme["btn_flip_txt"], width=2)
    draw.text((260, 810), "Перевернуть", fill=theme["btn_flip_txt"], font=font_btn)

    # Known Button (Soft 3D Carved)
    img = draw_neumorphic_card(img, [(430, 760), (595, 850)], theme["card_bg"], theme["shadow_dark"], theme["shadow_light"], radius=24)
    draw = ImageDraw.Draw(img)
    # Checkmark icon
    cx, cy = 512, 785
    draw.ellipse([(cx - 10, cy - 10), (cx + 10, cy + 10)], outline=acc_green, width=2)
    draw.line([(cx - 5, cy), (cx - 1, cy + 4)], fill=acc_green, width=2)
    draw.line([(cx - 1, cy + 4), (cx + 6, cy - 4)], fill=acc_green, width=2)
    draw.text((485, 810), "Знаю", fill=acc_green, font=font_btn)

    # 6. Bottom Dock (Long 3D Raised Soft Bar)
    img = draw_neumorphic_card(img, [(55, 1005), (585, 1085)], theme["card_bg"], theme["shadow_dark"], theme["shadow_light"], radius=28)
    draw = ImageDraw.Draw(img)
    draw.text((120, 1035), "Карточки", fill=acc, font=font_med)
    draw.text((290, 1035), "Словарь", fill=c_sub, font=font_med)
    draw.text((440, 1035), "Прогресс", fill=c_sub, font=font_med)

    out_file = os.path.join(ARTIFACTS_DIR, f"wood_mockup_{theme['id']}.png")
    img.save(out_file, "PNG")
    return out_file

def generate_wood_presentation():
    mockup_files = {}
    for t in WOOD_THEMES:
        mockup_files[t["id"]] = render_wood_mockup(t)

    pdf_file = os.path.join(OUTPUT_DIR, "Wood_Clay_Neumorphic_Themes.pdf")
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
        textColor=colors.HexColor('#3E2F24'),
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'MainSubTitle',
        fontName='Arial',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#8D6E53'),
        spaceAfter=10
    )
    desc_style = ParagraphStyle(
        'DescP',
        fontName='Arial',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor('#4A3C31')
    )

    # -------------------------------------------------------------------------
    # PAGE 1: Themes 1 & 2 (Birch Wood Light & Smoked Walnut Dark)
    # -------------------------------------------------------------------------
    story.append(Paragraph("🪵 WOW English — Стиль «Тактильное дерево и мягкая глина»", title_style))
    story.append(Paragraph("Концепт разработан по вашему новому референсу: мягкий 3D-барельеф (Neumorphism), фактура гладкого светлого дерева/бука и тёплой глины, выдавленные тактильные кнопки без резких теней.", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#D7CCC8'), spaceAfter=10))

    img_w, img_h = 245, 436

    d1 = f"""
    <b>ВАРИАНТ №1: {WOOD_THEMES[0]['title']}</b><br/>
    <font color="#A87855"><b>☀️ СВЕТЛАЯ ТЕМА (Светлое дерево и тёплая глина)</b></font><br/><br/>
    • <b>Фактура:</b> Скандинавский светлый бук и тёплая глина (<code>#EFE8DE</code>).<br/>
    • <b>Эффект:</b> Мягкий объёмный 3D-барельеф с плавным двойным светом.<br/>
    • <b>Иконки:</b> Гравировка вглубь поверхности в тонах тика и шалфея.<br/>
    • <b>Атмосфера:</b> Тёплый тактильный скандинавский интерьер, невероятный уют.
    """

    d2 = f"""
    <b>ВАРИАНТ №2: {WOOD_THEMES[1]['title']}</b><br/>
    <font color="#DAA26C"><b>🌙 ТЁМНАЯ ТЕМА (Мореный тёмный дуб и орех)</b></font><br/><br/>
    • <b>Фактура:</b> Глубокое мореное дерево и обожжённый дуб (<code>#201B17</code>).<br/>
    • <b>Эффект:</b> Мягкая бархатная глубина и выдавленные деревянные плитки.<br/>
    • <b>Иконки:</b> Тёплый янтарный свет камина и мягкий лесной мох.<br/>
    • <b>Атмосфера:</b> Спокойный вечер в деревянном шале у камина.
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
    # PAGE 2: Themes 3 & 4 (Honey Oak & Nordic Pine)
    # -------------------------------------------------------------------------
    story.append(Paragraph("Альтернативные древесные полутона (Варианты 3 и 4)", title_style))
    story.append(Paragraph("Медовый золотистый дуб и глубокая хвойная северная сосна:", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#D7CCC8'), spaceAfter=10))

    d3 = f"""
    <b>ВАРИАНТ №3: {WOOD_THEMES[2]['title']}</b><br/>
    <font color="#B9824E"><b>☀️ СВЕТЛАЯ ТЕМА (Медовый дуб и лён)</b></font><br/><br/>
    • <b>Фактура:</b> Солнечный медовый дуб и натуральный лён (<code>#F5EFE6</code>).<br/>
    • <b>Эффект:</b> Мягкий янтарный свет, бархатистая поверхность.<br/>
    • <b>Атмосфера:</b> Тёплый солнечный свет через деревянные жалюзи.
    """

    d4 = f"""
    <b>ВАРИАНТ №4: {WOOD_THEMES[3]['title']}</b><br/>
    <font color="#7DB287"><b>🌙 ТЁМНАЯ ТЕМА (Северная сосна и мох)</b></font><br/><br/>
    • <b>Фактура:</b> Тёмное хвойное дерево и лесной мох (<code>#1A201C</code>).<br/>
    • <b>Эффект:</b> Природный хвойный полумрак с мягкой шалфейной подсветкой.<br/>
    • <b>Атмосфера:</b> Абсолютный природный релакс для вечерних занятий.
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
    # PAGE 3: Особенности Neumorphic-дизайна
    # -------------------------------------------------------------------------
    story.append(Paragraph("🔍 Как устроен эффект дерева и глины (Neumorphism)", title_style))
    story.append(Paragraph("В этом стиле плоские кнопки превращаются в объёмные физические объекты:", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#D7CCC8'), spaceAfter=10))

    tech_details = [
        [
            Paragraph("<b>Элемент</b>", desc_style),
            Paragraph("<b>Как это реализовано в интерфейсе</b>", desc_style),
            Paragraph("<b>Ощущение при использовании</b>", desc_style)
        ],
        [
            Paragraph("Карточка со словами", desc_style),
            Paragraph("Выпуклая 3D-плитка со скруглением 36px, двойной мягкой тенью и светящимся верхним скосом.", desc_style),
            Paragraph("Ощущается как отшлифованная деревянная дощечка или керамическая плитка.", desc_style)
        ],
        [
            Paragraph("Переключатель фильтров", desc_style),
            Paragraph("Вдавленная выемка в дереве (деревянное русло), в котором скользит выпуклая плашка.", desc_style),
            Paragraph("Настоящий аналоговый тактильный слайдер.", desc_style)
        ],
        [
            Paragraph("Кнопки «Учу», «Знаю», «Flip»", desc_style),
            Paragraph("Выпуклые тактильные кнопки, которые при нажатии мягко вдавливаются внутрь (эффект клика на клавишу).", desc_style),
            Paragraph("Приятная обратная связь при каждом нажатии.", desc_style)
        ],
        [
            Paragraph("Иконки и надписи", desc_style),
            Paragraph("Тонкая гравировка (emboss/deboss) строго в тонах натурального дерева и глины.", desc_style),
            Paragraph("Никаких ярких цветов — полная гармония и визуальный покой.", desc_style)
        ]
    ]

    tech_tbl = Table(tech_details, colWidths=[120, 210, 200])
    tech_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#EFEBE9')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D7CCC8')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FAF8F6'), colors.HexColor('#FFFFFF')]),
    ]))
    story.append(tech_tbl)

    story.append(Spacer(1, 16))

    callout_p = Paragraph(
        "💡 <b>Готовы применить этот тактильный деревянный стиль?</b><br/>"
        "Напишите мне: <b>«Да, давай применим вариант №1 (или №2) под дерево»</b> — и я активирую этот мягкий неоморфный барельеф прямо в приложении!",
        desc_style
    )
    callout_tbl = Table([[callout_p]], colWidths=[530])
    callout_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EFEBE9')),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#A87855')),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(callout_tbl)

    doc.build(story)
    print("Wood & Clay PDF built:", pdf_file)

    root_pdf = r'c:\PROJECTS\WOW_English_Wood_Clay_Theme.pdf'
    shutil.copyfile(pdf_file, root_pdf)
    print("Copied to root:", root_pdf)

if __name__ == '__main__':
    generate_wood_presentation()
