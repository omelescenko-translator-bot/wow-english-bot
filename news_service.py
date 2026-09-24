# -*- coding: utf-8 -*-
"""
News & Context Texts Service for Language Learning Bot
Finds real internet news / articles containing vocabulary words,
or synthesizes engaging, authentic news and stories covering 100% of the selected words.
"""

import os
import sys
import re
import html
import random
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import requests
import logging

try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

from translator import smart_translate, translate_fallback_gtx, translate_fallback_mymemory

logger = logging.getLogger(__name__)

TOPIC_CONFIGS = [
    {
        "topic": "🎬 Звёзды & Шоубиз",
        "sources": ["The Hollywood Reporter", "People Magazine", "Variety", "E! News", "Vogue"],
        "themes": ["film festival", "red carpet", "celebrity interview", "music award", "hollywood premiere"]
    },
    {
        "topic": "🚀 Технологии & Наука",
        "sources": ["TechCrunch", "Wired", "The Verge", "MIT Tech Review", "Ars Technica"],
        "themes": ["AI breakthrough", "smart gadgets", "space mission", "future robotics", "silicon valley update"]
    },
    {
        "topic": "💼 Бизнес & Карьера",
        "sources": ["Bloomberg", "CNBC", "Forbes", "Financial Times", "Wall Street Journal"],
        "themes": ["global market trend", "supply chain innovation", "startup success", "leadership strategy", "trade partnership"]
    },
    {
        "topic": "🌿 Стиль жизни & Путешествия",
        "sources": ["National Geographic", "BBC Culture", "Travel + Leisure", "Time Out", "The Guardian"],
        "themes": ["hidden destinations", "healthy habits", "cultural festival", "culinary journey", "modern city life"]
    },
    {
        "topic": "🌍 Мировые события",
        "sources": ["Reuters", "BBC News", "Associated Press", "EuroNews", "CNN International"],
        "themes": ["international summit", "global eco project", "urban development", "cultural exchange", "community initiative"]
    }
]

def clean_html(raw_html: str) -> str:
    if not raw_html:
        return ""
    clean = re.sub(r'<[^>]+>', ' ', raw_html)
    clean = html.unescape(clean)
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean

def search_live_news_rss(query: str, lang: str = 'en') -> list:
    """Searches Google News RSS for real published news containing the query phrase."""
    try:
        clean_q = re.sub(r'[^\w\s]', '', query).strip()
        if not clean_q or len(clean_q) < 2:
            return []
            
        encoded = urllib.parse.quote(f'"{clean_q}"')
        url = f"https://news.google.com/rss/search?q={encoded}&hl=en-US&gl=US&ceid=US:en"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        resp = requests.get(url, headers=headers, timeout=4)
        if resp.status_code == 200:
            root = ET.fromstring(resp.content)
            items = root.findall('.//item')
            results = []
            for it in items[:4]:
                title = it.find('title').text if it.find('title') is not None else ''
                desc = it.find('description').text if it.find('description') is not None else ''
                source = it.find('source').text if it.find('source') is not None else 'Live News'
                clean_title = clean_html(title)
                clean_desc = clean_html(desc)
                
                # Split and clean
                if ' - ' in clean_title:
                    clean_title = clean_title.rsplit(' - ', 1)[0].strip()
                    
                if clean_title:
                    results.append({
                        "title": clean_title,
                        "snippet": clean_desc,
                        "source": source
                    })
            return results
    except Exception as e:
        logger.warning(f"Error fetching RSS news for '{query}': {e}")
    return []

def translate_story_text(text: str, src_lang: str = 'en', tgt_lang: str = 'ru') -> str:
    """Translates paragraph into native language."""
    if not text or src_lang == tgt_lang:
        return text
    try:
        # Use gtx fast translation
        trans = translate_fallback_gtx(text, src_lang, tgt_lang)
        if trans:
            return trans
        trans2 = translate_fallback_mymemory(text, src_lang, tgt_lang)
        if trans2:
            return trans2
    except Exception as e:
        logger.warning(f"Error translating story: {e}")
    return text

def build_story_passage(words_subset: list, topic_cfg: dict, real_news_item: dict = None, target_lang: str = 'en') -> dict:
    """
    Constructs a rich, cohesive, natural news or celebrity story in target_lang
    that embeds all phrases in words_subset with high realism and readability.
    """
    phrases_en = [w.get('phrase_en', '').strip() for w in words_subset if w.get('phrase_en')]
    topic_name = topic_cfg["topic"]
    source_name = real_news_item.get("source") if real_news_item else random.choice(topic_cfg["sources"])
    
    # Generate contextual paragraphs
    if "Звёзды" in topic_name:
        headline = real_news_item.get("title") if real_news_item else f"Exclusive Interview with Hollywood Stars on the Red Carpet"
        lead_templates = [
            f"During the latest international film festival, famous actors and directors gathered to share behind-the-scenes moments from their upcoming blockbuster.",
            f"At the glamorous evening premiere, the film cast spoke openly with reporters about teamwork, creative challenges, and their future plans.",
            f"Fans and critics were excited to hear from the movie crew after the red carpet ceremony yesterday in Venice."
        ]
    elif "Технологии" in topic_name:
        headline = real_news_item.get("title") if real_news_item else f"Tech Pioneers Unveil New Generation of Smart AI Systems"
        lead_templates = [
            f"Leading engineers and researchers presented their breakthrough platform at the annual technology summit in San Francisco today.",
            f"Silicon Valley developers announced a groundbreaking update designed to streamline everyday workflows and enhance communication.",
            f"The tech industry is witnessing a major transformation as new collaborative tools are being introduced across global teams."
        ]
    elif "Бизнес" in topic_name:
        headline = real_news_item.get("title") if real_news_item else f"Global Business Summit Focuses on Sustainable Growth and Logistics"
        lead_templates = [
            f"Industry leaders gathered at the international economic forum to discuss cross-border collaboration and operational efficiency.",
            f"Top executives highlighted the importance of clear coordination, timely deliveries, and reliable partnerships during quarterly meetings.",
            f"Modern trade networks are adapting to fast-paced market demands with innovative management and smart scheduling."
        ]
    elif "Путешествия" in topic_name:
        headline = real_news_item.get("title") if real_news_item else f"Discovering Hidden Gems: Cultural Journeys and Modern Lifestyle"
        lead_templates = [
            f"Travelers and lifestyle enthusiasts from around the world are sharing their favorite stories and practical tips for city exploration.",
            f"A new cultural report highlights how authentic local experiences and welcoming communities inspire travelers everywhere.",
            f"Exploring scenic historic streets and meeting inspiring people makes every journey a memorable and rewarding adventure."
        ]
    else:
        headline = real_news_item.get("title") if real_news_item else f"Global Forum Highlights New Innovations in International Collaboration"
        lead_templates = [
            f"Representatives from over thirty countries came together to discuss shared progress and community initiatives this week.",
            f"The international conference concluded with ambitious agreements on mutual support, cultural exchange, and sustainable projects.",
            f"Global leaders emphasized the power of transparent communication and joint teamwork in addressing modern challenges."
        ]

    lead = random.choice(lead_templates)
    
    # Weave the target phrases into natural, grammatically correct sentences
    sentences = [lead]
    
    # Combine phrases naturally
    phrase_connectors = [
        "In a keynote address, the team stated that \"{0}\" will be their main guiding principle.",
        "When asked about the key to their success, the spokesperson remarked: \"{0}\".",
        "Experts pointed out that everyone involved should \"{0}\" to achieve the best possible results.",
        "\"We always make sure to {0},\" added the director during the press briefing.",
        "One of the most discussed points was how to {0} efficiently in any situation.",
        "The project team agreed that \"{0}\" remains an essential step for upcoming milestones.",
        "Looking forward, participants agreed to \"{0}\" and continue building strong connections."
    ]
    random.shuffle(phrase_connectors)
    
    # If multiple phrases, we can also combine two into one sentence
    idx = 0
    while idx < len(phrases_en):
        p1 = phrases_en[idx]
        if idx + 1 < len(phrases_en) and random.random() > 0.4:
            p2 = phrases_en[idx + 1]
            combo_sentence = f"The organizers emphasized that we need to \"{p1}\" and at the same time \"{p2}\" to keep moving forward."
            sentences.append(combo_sentence)
            idx += 2
        else:
            conn = phrase_connectors[idx % len(phrase_connectors)]
            sentences.append(conn.format(p1))
            idx += 1
            
    sentences.append("The event concluded with positive reviews and widespread appreciation from attendees worldwide.")
    full_text_target = " ".join(sentences)

    return {
        "headline": headline,
        "topic": topic_name,
        "source": source_name,
        "text_target": full_text_target,
        "words": words_subset
    }

def generate_news_context_stories(words: list, target_lang: str = 'en', native_lang: str = 'ru') -> list:
    """
    Main entry point:
    Generates 1 or more rich news / context stories covering 100% of the input words.
    Partitions words into manageable clusters (2 to 5 words per story).
    """
    if not words:
        return []

    # Clean words list
    valid_words = [w for w in words if w.get('phrase_en') or w.get('phrase_ru')]
    if not valid_words:
        return []

    # Partition words into chunks (max 4-5 words per story so each text is concise and easy to read)
    chunk_size = 4 if len(valid_words) > 4 else len(valid_words)
    word_chunks = []
    for i in range(0, len(valid_words), chunk_size):
        word_chunks.append(valid_words[i:i + chunk_size])

    stories = []
    
    # Shuffle topic configs for variety
    topics_pool = list(TOPIC_CONFIGS)
    random.shuffle(topics_pool)

    for chunk_idx, chunk in enumerate(word_chunks):
        topic_cfg = topics_pool[chunk_idx % len(topics_pool)]
        
        # 1. Search for live internet news for the first phrase in this chunk
        real_news = None
        for w in chunk:
            en_phrase = w.get('phrase_en', '').strip()
            if en_phrase:
                # Try finding real online news
                found_items = search_live_news_rss(en_phrase, lang=target_lang)
                if found_items:
                    real_news = found_items[0]
                    break
        
        # 2. Build the cohesive story passage with all words in this chunk
        raw_story = build_story_passage(chunk, topic_cfg, real_news_item=real_news, target_lang=target_lang)
        
        # 3. Translate story into user's native language
        text_target = raw_story["text_target"]
        text_native = translate_story_text(text_target, src_lang=target_lang, tgt_lang=native_lang)
        
        # 4. Prepare target words list for this story
        target_words_list = []
        for w in chunk:
            target_words_list.append({
                "id": w.get("id", 0),
                "phrase_target": w.get("phrase_en", ""),
                "phrase_native": w.get("phrase_ru", "")
            })

        story_obj = {
            "id": f"story_{chunk_idx + 1}",
            "story_index": chunk_idx + 1,
            "total_stories": len(word_chunks),
            "title": raw_story["headline"],
            "topic": raw_story["topic"],
            "source": raw_story["source"],
            "text_target": text_target,
            "text_native": text_native,
            "target_words": target_words_list,
            "word_ids": [w.get("id") for w in chunk if w.get("id")],
            "has_real_web_source": bool(real_news)
        }
        stories.append(story_obj)

    return stories

if __name__ == '__main__':
    sample_words = [
        {"id": 1, "phrase_en": "Keep me in the loop", "phrase_ru": "Держи меня в курсе"},
        {"id": 2, "phrase_en": "Lead time", "phrase_ru": "Срок выполнения заказа"},
        {"id": 3, "phrase_en": "Red carpet", "phrase_ru": "Красная дорожка"},
        {"id": 4, "phrase_en": "Cut delivery times", "phrase_ru": "Сократить сроки доставки"},
        {"id": 5, "phrase_en": "Deal with it", "phrase_ru": "Справиться с этим"},
        {"id": 6, "phrase_en": "Break the ice", "phrase_ru": "Растопить лед в общении"},
        {"id": 7, "phrase_en": "Bill of lading", "phrase_ru": "Коносамент / транспортная накладная"}
    ]
    res = generate_news_context_stories(sample_words, target_lang='en', native_lang='ru')
    print(f"Generated {len(res)} stories covering {len(sample_words)} words:")
    for s in res:
        print("\n" + "="*50)
        print(f"[{s['topic']}] {s['title']} ({s['source']})")
        print(f"Words covered: {[w['phrase_target'] for w in s['target_words']]}")
        print("\n--- English ---")
        print(s['text_target'])
        print("\n--- Russian ---")
        print(s['text_native'])
