from transformers import pipeline

translator_pipeline = pipeline("translation", model="unicamp-dl/translation-en-pt-t5")

def translate_text(text):
    try:
        translated = translator_pipeline(text, max_length=512)
        return translated[0]['translation_text']
    except Exception as e:
        print(f"[Translator Error] {e}")
        return "Erro ao traduzir o resumo."