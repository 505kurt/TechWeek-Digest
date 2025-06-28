from transformers import pipeline

summarizer_pipeline = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text, max_length=160, min_length=80):
    text = text[:2000]
    if len(text) < 100:
        return "Texto muito curto para resumir."

    if not text or text.strip() == "":
        return "Texto vazio. Não foi possível gerar resumo."

    try:
        result = summarizer_pipeline(
            text,
            max_length=max_length,
            min_length=min_length,
            do_sample=False
        )
        return result[0]['summary_text']
    except Exception as e:
        print(f"[Summarizer Error] {e}")
        return "Erro ao gerar o resumo."