import spacy
import en_core_web_sm  # noqa: F401
import pytextrank  # noqa: F401


def summarize_text(text: str) -> str:
    """
    Summarize a PDF file
    """
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("textrank")

    doc = nlp(text)
    summary = [
        str(sentence).replace("\n", " ").replace("  ", " ")
        for sentence in doc._.textrank.summary()
    ]

    return "\n".join(summary)
