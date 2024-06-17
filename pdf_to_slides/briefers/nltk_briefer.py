# NLTK
# import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize


def nltk_summarizer(
    text: str = None, num_sentences: int = 3
) -> str:  # this was named : nltk_accurate_brief_en
    if text is None:
        return ""

    # Tokenize the text into sentences
    sentences = sent_tokenize(text)

    # Tokenize words and filter out stop words
    stop_words = set(stopwords.words("english"))
    word_frequencies = {}
    for sentence in sentences:
        words = word_tokenize(sentence.lower())
        for word in words:
            if word.isalnum() and word not in stop_words:
                if word in word_frequencies:
                    word_frequencies[word] += 1
                else:
                    word_frequencies[word] = 1

    # Score the sentences based on word frequencies
    sentence_scores = {}
    for sentence in sentences:
        score = 0
        words = word_tokenize(sentence.lower())
        for word in words:
            if word in word_frequencies:
                score += word_frequencies[word]
        sentence_scores[sentence] = score

    # Select the top n sentences
    sorted_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)
    summary_sentences = sorted_sentences[:num_sentences]

    # Combine the sentences into a single string
    result = " ".join(summary_sentences)

    return result
