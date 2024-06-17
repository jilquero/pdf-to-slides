from transformers import BartTokenizer, BartForConditionalGeneration


def bart_summarizer(
    text: str = None,
    max_length: int = 100,
    min_length: int = 50,
    length_penalty: float = 2.0,
    num_beams: int = 4,
) -> str:
    if text is None:
        return ""

    # Load pre-trained BART model and tokenizer
    model_name = "facebook/bart-large-cnn"
    tokenizer = BartTokenizer.from_pretrained(model_name)
    model = BartForConditionalGeneration.from_pretrained(model_name)

    # Tokenize and summarize the input text using BART
    inputs = tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(
        inputs["input_ids"],
        max_length=max_length,
        min_length=min_length,
        length_penalty=length_penalty,
        num_beams=num_beams,
        early_stopping=True,
    )

    # Decode and output the summary
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return summary
