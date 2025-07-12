import os 
import requests
from dotenv import load_dotenv

load_dotenv()
ACCOUNT_ID = os.getenv("ACCOUNT_ID")
API_TOKEN = os.getenv("API_TOKEN")

API_BASE_URL = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def run_summarizer(model, input):
    response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json=input)
    return response.json()

def summarize_text(text, max_length=160, min_length=80):
    text = text[:2000]
    if len(text) < 100:
        return "Texto muito curto para resumir."

    if not text or text.strip() == "":
        return "Texto vazio. Não foi possível gerar resumo."

    try:
        summarized = run_summarizer(
            "@cf/facebook/bart-large-cnn", {
                "input_text": text,
                'max_lenght': max_length,
                'min_lenght': min_length
            }
        )
        return summarized['result']['summary']
    except Exception as e:
        print(f"[Summarizer Error] {e}")
        return "Erro ao gerar o resumo."
    
if __name__ == "__main__":
    text = """
    OpenAI is an AI research and deployment company. Our mission is to ensure that artificial general intelligence (AGI)—
    highly autonomous systems that outperform humans at most economically valuable work—benefits all of humanity.
    We will build safe and beneficial AGI, or help others achieve this outcome.
    We commit to use any influence we have over AGI to ensure it is used for the benefit of all,
    and to avoid enabling uses that harm people or concentrate power unduly.
        """
    print(summarize_text(text))