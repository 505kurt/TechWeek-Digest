from flask import Flask

app = Flask(__name__)

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