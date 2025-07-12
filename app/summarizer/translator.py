"""
from transformers import pipeline

translator_pipeline = pipeline("translation", model="unicamp-dl/translation-en-pt-t5")

def translate_text(text):
    try:
        translated = translator_pipeline(text, max_length=512)
        return translated[0]['translation_text']
    except Exception as e:
        print(f"[Translator Error] {e}")
        return "Erro ao traduzir o resumo."
    """
import os 
import requests
from dotenv import load_dotenv

load_dotenv()
ACCOUNT_ID = os.getenv("ACCOUNT_ID")
API_TOKEN = os.getenv("API_TOKEN")

API_BASE_URL = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def run_translator(model, input):
    response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json=input)
    return response.json()

def translate_text(text):
    try:
        translated = run_translator('@cf/meta/m2m100-1.2b', {
            'text': text,
            'source_lang': 'en',
            'target_lang': 'pt'
        })
        return translated['result']['translated_text']
    except Exception as e:
        print(f"[Translator Error] {e}")
        return "Erro ao traduzir o resumo."
    
if __name__ == '__main__':
    print(translate_text("Hello my little friend."))