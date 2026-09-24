# -*- coding: utf-8 -*-
"""
Генератор PDF-визуализации на основе палитры из Pinterest референса:
- Светлый цвет: Warm Linen Cream & Natural Sage (#F6EFE9, #E5DCD1, #68866B, #D4A59A)
- Тёмный цвет: Deep Botanical Forest & Velvet Sage (#16241B, #223328, #7FA683, #E5B894)
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
REF_IMG = os.path.join(OUTPUT_DIR, 'pinterest_reference.jpg')

# 1. Render Light Theme Mockup (Pinterest Palette)
def render_pinterest_light():
    w, h = 640, 1138
    # Background: warm linen cream #F6EFE9
    img = PILImage.new('RGBA', (w, h), (246, 239, 233, 255))
    
    # Soft sage & peach auras
    overlay = PILImage.new('RGBA', (w, h), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    ov_draw.ellipse([(-40, -40), (420, 420)], fill=(212, 226, 214, 150)) # Sage aura
    ov_draw.ellipse([(280, 650), (700, 1050)], fill=(245, 220, 210, 130)) # Dusty peach aura
    overlay = overlay.filter(ImageFilter.GaussianBlur(55))
    img = PILImage.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    try:
        font_large = ImageFont.truetype(arial_bd_path, 36)
        font_med = ImageFont.truetype(arial_bd_path, 23)
        font_sub = ImageFont.truetype(arial_path, 21)
        font_small = ImageFont.truetype(arial_path, 17)
        font_btn = ImageFont.truetype(arial_bd_path, 20)
    except Exception:
        font_large = font_med = font_sub = font_small = font_btn = None

    c_main = (42, 47, 37)       # Deep Forest Espresso
    c_sub = (110, 118, 106)      # Muted Herbaceous Slate
    c_sage = (104, 134, 107)     # Botanical Sage
    c_peach = (212, 165, 154)    # Dusty Peach Rose
    c_card = (255, 253, 250)     # Clean Milk Porcelain
    c_border = (229, 220, 209)   # Linen Border
    c_chip = (238, 230, 222)     # Soft Taupe Chip

    # Header
    draw.ellipse([(45, 50), (95, 100)], fill=c_sage)
    draw.text((58, 63), "OM", fill=(255, 255, 255), font=font_med)
    draw.text((110, 58), "Olga M.", fill=c_main, font=font_med)
    draw.text((110, 82), "Aesthetic Learner", fill=c_sage, font=font_small)

    # Streak Badge
    draw.rounded_rectangle([(470, 55), (595, 95)], radius=20, fill=c_chip, outline=c_peach, width=2)
    draw.text((490, 63), "🔥 14 дн.", fill=(195, 110, 95), font=font_med)

    # Segmented Filter
    draw.rounded_rectangle([(45, 135), (595, 190)], radius=16, fill=c_chip, outline=c_border, width=1)
    draw.rounded_rectangle([(48, 138), (228, 187)], radius=13, fill=c_sage)
    draw.text((95, 150), "Все (76)", fill=(255, 255, 255), font=font_med)
    draw.text((275, 150), "⏳ Учу (62)", fill=c_sub, font=font_med)
    draw.text((450, 150), "✅ Знаю (14)", fill=c_sub, font=font_med)

    # Main Card
    card_bounds = [(45, 225), (595, 730)]
    draw.rounded_rectangle(card_bounds, radius=28, fill=c_card, outline=c_border, width=2)

    # Category Chip
    draw.rounded_rectangle([(75, 255), (310, 298)], radius=12, fill=c_chip, outline=c_border, width=1)
    draw.text((90, 266), "🌿 Деловая переписка", fill=c_sage, font=font_small)

    # Lang Pill + Speaker
    draw.rounded_rectangle([(415, 255), (515, 298)], radius=10, fill=(235, 245, 236), outline=c_sage, width=1)
    draw.text((430, 266), "ENGLISH", fill=c_sage, font=font_small)
    draw.ellipse([(530, 253), (572, 295)], fill=c_chip, outline=c_sage, width=1)
    draw.text((542, 263), "🎧", fill=c_sage, font=font_small)

    # Phrase Text
    draw.text((75, 360), "Shorten the lead time", fill=c_main, font=font_large)
    draw.text((75, 408), "for the next order.", fill=c_main, font=font_large)

    draw.text((75, 500), "Сократить срок поставки", fill=c_sub, font=font_sub)
    draw.text((75, 530), "для следующего заказа.", fill=c_sub, font=font_sub)

    # Hint Pill
    draw.rounded_rectangle([(160, 660), (480, 698)], radius=16, fill=c_chip, outline=c_border, width=1)
    draw.text((180, 670), "👆 Нажмите, чтобы перевернуть", fill=c_sub, font=font_small)

    # Action Controls
    # Repeat / Learning
    draw.rounded_rectangle([(45, 765), (210, 855)], radius=20, fill=c_chip, outline=c_peach, width=2)
    draw.text((115, 780), "⏳", fill=(195, 110, 95), font=font_med)
    draw.text((100, 812), "Учу", fill=(195, 110, 95), font=font_btn)

    # Flip
    draw.rounded_rectangle([(230, 765), (410, 855)], radius=20, fill=c_sage)
    draw.text((305, 780), "🔄", fill=(255, 255, 255), font=font_med)
    draw.text((265, 812), "Перевернуть", fill=(255, 255, 255), font=font_btn)

    # Known
    draw.rounded_rectangle([(430, 765), (595, 855)], radius=20, fill=(235, 245, 236), outline=c_sage, width=2)
    draw.text((500, 780), "✅", fill=c_sage, font=font_med)
    draw.text((485, 812), "Знаю", fill=c_sage, font=font_btn)

    # Bottom Dock
    draw.rounded_rectangle([(55, 1010), (585, 1090)], radius=26, fill=c_card, outline=c_border, width=1)
    draw.text((115, 1037), "🃏 Карточки", fill=c_sage, font=font_med)
    draw.text((295, 1037), "📖 Словарь", fill=c_sub, font=font_med)
    draw.text((455, 1037), "🔥 Прогресс", fill=c_sub, font=font_med)

    out_file = os.path.join(ARTIFACTS_DIR, "pinterest_theme_light.png")
    img.save(out_file, "PNG")
    return out_file

# 2. Render Dark Theme Mockup (Pinterest Palette)
def render_pinterest_dark():
    w, h = 640, 1138
    # Background: deep botanical forest #16241B
    img = PILImage.new('RGBA', (w, h), (22, 36, 27, 255))
    
    # Soft deep moss auras
    overlay = PILImage.new('RGBA', (w, h), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    ov_draw.ellipse([(-30, -30), (420, 420)], fill=(45, 75, 55, 140))
    ov_draw.ellipse([(280, 650), (700, 1050)], fill=(70, 60, 40, 110))
    overlay = overlay.filter(ImageFilter.GaussianBlur(55))
    img = PILImage.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    try:
        font_large = ImageFont.truetype(arial_bd_path, 36)
        font_med = ImageFont.truetype(arial_bd_path, 23)
        font_sub = ImageFont.truetype(arial_path, 21)
        font_small = ImageFont.truetype(arial_path, 17)
        font_btn = ImageFont.truetype(arial_bd_path, 20)
    except Exception:
        font_large = font_med = font_sub = font_small = font_btn = None

    c_main = (244, 239, 234)     # Warm Linen Cream Text
    c_sub = (150, 175, 160)      # Soft Sage Grey Subtext
    c_sage = (127, 166, 131)     # Matcha Sage Light
    c_peach = (229, 184, 148)    # Warm Sand Peach
    c_card = (34, 51, 40)        # Deep Moss Glass Card
    c_border = (55, 82, 65)      # Botanical Border
    c_chip = (28, 44, 34)        # Deep Forest Chip

    # Header
    draw.ellipse([(45, 50), (95, 100)], fill=c_sage)
    draw.text((58, 63), "OM", fill=(22, 36, 27), font=font_med)
    draw.text((110, 58), "Olga M.", fill=c_main, font=font_med)
    draw.text((110, 82), "Botanical Mode", fill=c_sage, font=font_small)

    # Streak Badge
    draw.rounded_rectangle([(470, 55), (595, 95)], radius=20, fill=c_chip, outline=c_peach, width=2)
    draw.text((490, 63), "🔥 14 дн.", fill=c_peach, font=font_med)

    # Segmented Filter
    draw.rounded_rectangle([(45, 135), (595, 190)], radius=16, fill=c_chip, outline=c_border, width=1)
    draw.rounded_rectangle([(48, 138), (228, 187)], radius=13, fill=c_sage)
    draw.text((95, 150), "Все (76)", fill=(22, 36, 27), font=font_med)
    draw.text((275, 150), "⏳ Учу (62)", fill=c_sub, font=font_med)
    draw.text((450, 150), "✅ Знаю (14)", fill=c_sub, font=font_med)

    # Main Card
    card_bounds = [(45, 225), (595, 730)]
    draw.rounded_rectangle(card_bounds, radius=28, fill=c_card, outline=c_border, width=2)

    # Category Chip
    draw.rounded_rectangle([(75, 255), (310, 298)], radius=12, fill=c_chip, outline=c_border, width=1)
    draw.text((90, 266), "🌿 Деловая переписка", fill=c_sage, font=font_small)

    # Lang Pill + Speaker
    draw.rounded_rectangle([(415, 255), (515, 298)], radius=10, fill=c_chip, outline=c_sage, width=1)
    draw.text((430, 266), "ENGLISH", fill=c_sage, font=font_small)
    draw.ellipse([(530, 253), (572, 295)], fill=c_chip, outline=c_sage, width=1)
    draw.text((542, 263), "🎧", fill=c_sage, font=font_small)

    # Phrase Text
    draw.text((75, 360), "Shorten the lead time", fill=c_main, font=font_large)
    draw.text((75, 408), "for the next order.", fill=c_main, font=font_large)

    draw.text((75, 500), "Сократить срок поставки", fill=c_sub, font=font_sub)
    draw.text((75, 530), "для следующего заказа.", fill=c_sub, font=font_sub)

    # Hint Pill
    draw.rounded_rectangle([(160, 660), (480, 698)], radius=16, fill=c_chip, outline=c_border, width=1)
    draw.text((180, 670), "👆 Нажмите, чтобы перевернуть", fill=c_sub, font=font_small)

    # Action Controls
    # Repeat / Learning
    draw.rounded_rectangle([(45, 765), (210, 855)], radius=20, fill=c_chip, outline=c_peach, width=2)
    draw.text((115, 780), "⏳", fill=c_peach, font=font_med)
    draw.text((100, 812), "Учу", fill=c_peach, font=font_btn)

    # Flip
    draw.rounded_rectangle([(230, 765), (410, 855)], radius=20, fill=c_sage)
    draw.text((305, 780), "🔄", fill=(22, 36, 27), font=font_med)
    draw.text((265, 812), "Перевернуть", fill=(22, 36, 27), font=font_btn)

    # Known
    draw.rounded_rectangle([(430, 765), (595, 855)], radius=20, fill=c_chip, outline=c_sage, width=2)
    draw.text((500, 780), "✅", fill=c_sage, font=font_med)
    draw.text((485, 812), "Знаю", fill=c_sage, font=font_btn)

    # Bottom Dock
    draw.rounded_rectangle([(55, 1010), (585, 1090)], radius=26, fill=c_card, outline=c_border, width=1)
    draw.text((115, 1037), "🃏 Карточки", fill=c_sage, font=font_med)
    draw.text((295, 1037), "📖 Словарь", fill=c_sub, font=font_med)
    draw.text((455, 1037), "🔥 Прогресс", fill=c_sub, font=font_med)

    out_file = os.path.join(ARTIFACTS_DIR, "pinterest_theme_dark.png")
    img.save(out_file, "PNG")
    return out_file

def build_pinterest_pdf():
    img_light = render_pinterest_light()
    img_dark = render_pinterest_dark()

    pdf_file = os.path.join(OUTPUT_DIR, "Pinterest_Palette_Visualization.pdf")
    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=A4,
        leftMargin=30,
        rightMargin=30,
        topMargin=30,
        bottomMargin=30
    )

    story = []

    title_style = ParagraphStyle(
        'MainTitle',
        fontName='Arial-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#1E2B22'),
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'MainSubTitle',
        fontName='Arial',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#5B705C'),
        spaceAfter=10
    )
    sec_h2 = ParagraphStyle(
        'SecH2',
        fontName='Arial-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#1E2B22'),
        spaceBefore=4,
        spaceAfter=4
    )
    desc_style = ParagraphStyle(
        'DescP',
        fontName='Arial',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor('#334135')
    )

    story.append(Paragraph("🌿 WOW English — Визуализация по вашему Pinterest референсу", title_style))
    story.append(Paragraph("Оттенки из референса: натуральный льняной крем (#F6EFE9, #E5DCD1) и глубокий хвойно-оливковый (#16241B, #223328) с акцентами мягкого шалфея (#68866B) и пудрового персика (#D4A59A).", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=10))

    # Page 1: Side by side comparison (Light vs Dark)
    img_w, img_h = 245, 436

    desc_light = """
    <b>ВАРИАНТ А: «Linen Cream & Botanical Sage»</b><br/>
    <font color="#5B705C"><b>☀️ СВЕТЛАЯ ТЕМА (По референсу)</b></font><br/><br/>
    • <b>Фон:</b> Мягкий тёплый льняной крем (<code>#F6EFE9</code>).<br/>
    • <b>Карточка:</b> Молочный фарфор (<code>#FFFDFB</code>) с каймой льна (<code>#E5DCD1</code>).<br/>
    • <b>Акценты:</b> Натуральный шалфей-матча (<code>#68866B</code>) и пудровый персик (<code>#D4A59A</code>).<br/>
    • <b>Атмосфера:</b> Тёплый эко-уют, спокойствие, нулевая усталость глаз.
    """

    desc_dark = """
    <b>ВАРИАНТ Б: «Deep Forest & Velvet Sage»</b><br/>
    <font color="#7FA683"><b>🌙 ТЁМНАЯ ТЕМА (По референсу)</b></font><br/><br/>
    • <b>Фон:</b> Бархатный хвойно-оливковый (<code>#16241B</code>).<br/>
    • <b>Карточка:</b> Матовое лесное стекло (<code>#223328</code>) с каймой шалфея (<code>#375241</code>).<br/>
    • <b>Акценты:</b> Светящийся шалфей (<code>#7FA683</code>) и тёплый персиковый песок (<code>#E5B894</code>).<br/>
    • <b>Атмосфера:</b> Глубокий расслабляющий ночной комфорт без синего излучения.
    """

    table_row1 = [Image(img_light, width=img_w, height=img_h), Image(img_dark, width=img_w, height=img_h)]
    table_row2 = [Paragraph(desc_light, desc_style), Paragraph(desc_dark, desc_style)]

    tbl = Table([table_row1, table_row2], colWidths=[265, 265])
    tbl.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(tbl)

    story.append(PageBreak())

    # Page 2: Color Palette Swatches & Reference Breakdown
    story.append(Paragraph("🎨 Раскладка цветовой палитры из Pinterest", title_style))
    story.append(Paragraph("Точные HEX-коды и распределение цветов по элементам интерфейса:", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=12))

    # Reference Image + Palette Table
    ref_table_data = [
        [
            Image(REF_IMG, width=160, height=160),
            Paragraph(
                "<b>Исходный референс из Pinterest:</b><br/>"
                "• <b>Доминирующие цвета:</b> Тёплый льняной беж, мягкий шалфей-матча, тёмный хвойный мох, пудровый персиково-розовый.<br/>"
                "• <b>Ключевая идея:</b> Природная мягкость, отсутствие резких контрастов, ощущение уюта и тактильного комфорта.<br/>"
                "• <b>Применение:</b> Светлая тема берёт за основу кремово-льняной фон с шалфеем, а тёмная тема — бархатный лесной фон с мягкой подсветкой.",
                desc_style
            )
        ]
    ]
    ref_tbl = Table(ref_table_data, colWidths=[175, 355])
    ref_tbl.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(ref_tbl)

    story.append(Spacer(1, 16))

    story.append(Paragraph("Таблица цветов интерфейса:", sec_h2))

    swatch_data = [
        [
            Paragraph("<b>Элемент интерфейса</b>", desc_style),
            Paragraph("<b>Светлая тема (Linen Cream)</b>", desc_style),
            Paragraph("<b>Тёмная тема (Deep Forest)</b>", desc_style),
            Paragraph("<b>Роль в дизайне</b>", desc_style)
        ],
        [
            Paragraph("Основной фон", desc_style),
            Paragraph("<code>#F6EFE9</code> (Льняной крем)", desc_style),
            Paragraph("<code>#16241B</code> (Бархатная хвоя)", desc_style),
            Paragraph("Мягкая база экрана без усталости глаз", desc_style)
        ],
        [
            Paragraph("Карточка фраз", desc_style),
            Paragraph("<code>#FFFDFB</code> (Молочный фарфор)", desc_style),
            Paragraph("<code>#223328</code> (Лесное стекло)", desc_style),
            Paragraph("Главный фокус внимания с парящей тенью", desc_style)
        ],
        [
            Paragraph("Основной текст", desc_style),
            Paragraph("<code>#2A2F25</code> (Тёмный эспрессо)", desc_style),
            Paragraph("<code>#F4EFEA</code> (Льняной светлый)", desc_style),
            Paragraph("Максимальная четкость чтения слов", desc_style)
        ],
        [
            Paragraph("Главный акцент (Flip / Tabs)", desc_style),
            Paragraph("<code>#68866B</code> (Шалфей матча)", desc_style),
            Paragraph("<code>#7FA683</code> (Мягкий шалфей)", desc_style),
            Paragraph("Кнопка переворота, активные табы и док", desc_style)
        ],
        [
            Paragraph("Кнопка «Знаю ✅»", desc_style),
            Paragraph("<code>#5B705C</code> (Природная зелень)", desc_style),
            Paragraph("<code>#7FA683</code> (Шалфей)", desc_style),
            Paragraph("Мягкое подтверждение выученного слова", desc_style)
        ],
        [
            Paragraph("Кнопка «Учу ⏳» / Серия", desc_style),
            Paragraph("<code>#D4A59A</code> (Пыльный персик)", desc_style),
            Paragraph("<code>#E5B894</code> (Песочная охра)", desc_style),
            Paragraph("Тёплый уютный акцент повторения и Streak", desc_style)
        ]
    ]

    swatch_tbl = Table(swatch_data, colWidths=[110, 140, 140, 140])
    swatch_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8DFD8')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FAF7F2'), colors.HexColor('#FFFFFF')]),
    ]))
    story.append(swatch_tbl)

    story.append(Spacer(1, 16))

    callout_p = Paragraph(
        "💡 <b>Готовы применить эту палитру?</b><br/>"
        "Напишите: <b>«Да, примени эту тему из Pinterest»</b> — и я мгновенно обновлю стили приложения в этих точных благородных льняных и хвойно-шалфейных оттенках!",
        desc_style
    )
    callout_tbl = Table([[callout_p]], colWidths=[530])
    callout_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EBF3EC')),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#68866B')),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(callout_tbl)

    doc.build(story)
    print("Pinterest PDF created successfully:", pdf_file)

    root_pdf = r'c:\PROJECTS\WOW_English_Pinterest_Theme.pdf'
    shutil.copyfile(pdf_file, root_pdf)
    print("Copied to root:", root_pdf)

if __name__ == '__main__':
    build_pinterest_pdf()
