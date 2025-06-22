from app import app
from app.scraper.scraper import get_tech_news
from flask import jsonify

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