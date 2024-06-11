from transformers import PegasusForConditionalGeneration, PegasusTokenizer, pipeline
from transformers import T5ForConditionalGeneration, T5Tokenizer, pipeline
import torch
def summarize_google(text):
    # Ręczne ładowanie modelu i tokenizer
    model_name = "google/pegasus-large"
    model = PegasusForConditionalGeneration.from_pretrained(model_name)
    tokenizer = PegasusTokenizer.from_pretrained(model_name)

    # Inicjalizacja pipeline do podsumowywania
    summarizer = pipeline("summarization", model=model, tokenizer=tokenizer, framework="pt")

    # Podziel tekst na krótsze fragmenty
    max_chunk_length = 1024  # Maksymalna długość sekwencji dla modelu PEGASUS
    sentences = text.split('. ')
    current_chunk = ""
    chunks = []

    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 <= max_chunk_length:
            current_chunk += sentence + ". "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "
    if current_chunk:
        chunks.append(current_chunk.strip())

    # Generuj podsumowanie dla każdego fragmentu
    summaries = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=150, min_length=50, do_sample=False)
        summaries.append(summary[0]['summary_text'])

    # Połącz wszystkie podsumowania
    final_summary = ' '.join(summaries)
    print("Podsumowanie:")
    print(final_summary)

#Tutaj T5 się zaczyna
def post_process_summary(summary):
    # Usuń spacje przed kropkami
    summary = summary.replace(' .', '.')
    # Podziel podsumowanie na zdania
    sentences = summary.split('. ')
    # Upewnij się, że każde zdanie zaczyna się wielką literą
    sentences = [sentence.capitalize() for sentence in sentences]
    # Połącz zdania z powrotem do jednego tekstu
    processed_summary = '. '.join(sentences)
    return processed_summary

def summarize_t5(text):
    # Ręczne ładowanie modelu i tokenizer
    model_name = "t5-large"
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    tokenizer = T5Tokenizer.from_pretrained(model_name, legacy=False)

    # Inicjalizacja pipeline do podsumowywania
    device = 0 if torch.cuda.is_available() else -1
    summarizer = pipeline("summarization", model=model, tokenizer=tokenizer, framework="pt", device=device)

    # Podziel tekst na krótsze fragmenty
    max_chunk_length = 512  # Maksymalna długość sekwencji dla modelu T5
    sentences = text.split('. ')
    current_chunk = ""
    chunks = []

    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 <= max_chunk_length:
            current_chunk += sentence + ". "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "
    if current_chunk:
        chunks.append(current_chunk.strip())

    # Generuj podsumowanie dla każdego fragmentu
    summaries = []
    for chunk in chunks:
        input_length = len(tokenizer.encode(chunk, return_tensors="pt")[0])
        max_len = min(300, input_length)  # Dostosuj max_length do długości fragmentu
        min_len = max(50, input_length // 2)  # Dostosuj min_length do długości fragmentu
        if max_len <= min_len:
            max_len = min_len + 20  # Zapewnia różnicę między min a max długością
        summary = summarizer(chunk, max_length=max_len, min_length=min_len, do_sample=False)
        processed_summary = post_process_summary(summary[0]['summary_text'])
        summaries.append(processed_summary)

    # Połącz wszystkie podsumowania
    final_summary = ' '.join(summaries)
    return final_summary