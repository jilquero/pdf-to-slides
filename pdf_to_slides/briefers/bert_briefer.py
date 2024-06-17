# BERT - Bidirectional Encoder Representations from Transformers
# import bert
from summarizer import Summarizer


def bert_summarizer(
    input_text: str, min_length: int = 50, max_length: int = 150
) -> str:
    """
    Generate a summary of the input text using BERT extractive summarization.

    Args:
    input_text (str): The input text to be summarized.
    min_length (int): Minimum length of the summary.
    max_length (int): Maximum length of the summary.

    Returns:
    str: The generated summary.
    """
    # Create a BERT extractive summarizer
    summarizer_model = Summarizer()

    # Generate the summary
    summary = summarizer_model(input_text)

    return summary
