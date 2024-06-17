import spacy
from spacy.language import Language


def spacy_accurate_brief_en(text: str = None, num_sentences: int = 3) -> str:
    if text is None:
        return ""

    nlp = spacy.load("en_core_web_md", disable=["ner"])  # en_core_web_trf

    # nlp.remove_pipe('ner')
    nlp.add_pipe("textrank")

    print(nlp.pipe_names)

    doc = nlp(text)  # Process the text

    # Extract the most important sentences using pytextrank
    summary_sentences = []
    for sent in doc._.textrank.summary(limit_sentences=num_sentences):
        summary_sentences.append(sent.text)

    result = " ".join(summary_sentences)
    return result


# token scorer - scoring tokens between each other for most synthentically, thought that will essence the sentence,
# but it prints out the most connected  words (the words that most connected to each other)
def token_scorer(text: str = None) -> str:
    if text is None:
        return "--None text selected--"

    nlp = spacy.load("en_core_web_md")

    # Define the similarity checker pipe
    @Language.component("similarity_checker")
    def similarity_checker(doc):
        threshold = 11  # Adjust the threshold as per your liking
        filtered_tokens = []

        for sent in doc.sents:
            similarity_scores = []

            # Calculate the similarity scores for each token in the sentence
            for token in sent:
                similarity_score = 0
                for other_token in sent:
                    if token != other_token:
                        similarity_score += token.similarity(other_token)
                similarity_scores.append((token, similarity_score))

            sorted_tokens = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

            # Filter tokens based on the threshold
            filtered_tokens.extend(
                [token for token, score in sorted_tokens if score >= threshold]
            )

        # Create a new document with the filtered tokens
        doc = spacy.tokens.Doc(
            nlp.vocab, words=[token.text for token in filtered_tokens]
        )
        return doc

    nlp.add_pipe("similarity_checker", last=True)

    doc = nlp(text)

    result = [token.text for token in doc]
    return result
