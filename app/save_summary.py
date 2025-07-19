import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
API_URL = os.environ.get("API_URL")
LIMIT = 10

def run_job():
    try:
        resp = requests.get(f"{API_URL}/news/summary", timeout=90)
        resp.raise_for_status()
        summary = resp.json()

        save_resp = requests.post(f"{API_URL}/news/save", json=summary, timeout=30)
        save_resp.raise_for_status()

        print("[Job] Resumo salvo com sucesso.")

    except Exception as e:
        print(f"[Job] Erro ao atualizar resumo: {e}")

if __name__ == "__main__":
    run_job()