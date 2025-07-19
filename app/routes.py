import os
import json
from app import app
from app.scraper.scraper import get_tech_news, get_article_text
from app.summarizer.summarizer import summarize_text
from app.summarizer.translator import translate_text
from app.save_summary import run_job
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

@app.route('/news/save', methods=['POST'])
def save_cached_summary():
    data = request.get_json()
    with open("cached_summary.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return jsonify({"status": "Resumo salvo com sucesso"})

@app.route('/news/save', methods=['GET'])
def get_cached_summary():
    if not os.path.exists("cached_summary.json"):
        return jsonify({"error": "Resumo ainda não está disponível."}), 503

    with open("cached_summary.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    return jsonify(data)

@app.route('/cron-job', methods=['post'])
def cache_summary():
    run_job()