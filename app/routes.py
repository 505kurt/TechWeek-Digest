from app import app
from app.scraper.scraper import get_tech_news, get_article_text
from app.summarizer.summarizer import summarize_text
from app.summarizer.translator import translate_text
from flask import jsonify, request

@app.route("/")
def home():
    return {
        "status": "ok", 
        "message": "TechWeek Digest API - Phase 1"
        }

@app.route("/status")
def status():
    return {
        "status": "online",
        "app": "TechWeek Digest API",
        "version": "1.0.0",
        "environment": "development"
    }

@app.route('/news/raw')
def raw_news():
    news = get_tech_news()

    if isinstance(news, dict) and 'error' in news:
        return jsonify(news), 500

    return jsonify({"news": news})

@app.route('/news/summary')
def summarized_news():
    limit = request.args.get('limit', default=10, type=int)

    raw_news = get_tech_news()
    summarized_list = []

    for news in raw_news[:limit]:
        text = get_article_text(news['link'])

        if text.startswith("Erro") or text.startswith("Não foi possível"):
            continue

        summary = summarize_text(text)

        if news['source'] in ['TechCrunch']:
            title = translate_text(news['title'])
            summary = translate_text(summary)

        else:
            title = news['title']

        summarized_list.append({
            'title': title,
            'link': news['link'],
            'source': news['source'],
            'summary': summary
        })

    return jsonify({"news": summarized_list})
