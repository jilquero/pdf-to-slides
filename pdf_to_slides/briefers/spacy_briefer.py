import spacy
import pytextrank



def spacy_accurate_brief_en(text: str=None, num_sentences: int = 3) -> str:
    if text is None:
        return ""

    # Load the spaCy model and add pytextrank to the pipeline
    nlp = spacy.load("en_core_web_trf")
    nlp.add_pipe("textrank")

    # Process the text
    doc = nlp(text)

    # Extract the most important sentences using pytextrank
    summary_sentences = []
    for sent in doc._.textrank.summary(limit_sentences=num_sentences):
        summary_sentences.append(sent.text)
    
    # Combine the sentences into a single string
    result = ' '.join(summary_sentences)

    return result


