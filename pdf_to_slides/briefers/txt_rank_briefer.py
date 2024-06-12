import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx

def build_similarity_matrix(sentences, stop_words):
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i == j:  # Skip comparing a sentence with itself
                continue 
            similarity_matrix[i][j] = sentence_similarity(sentences[i], sentences[j], stop_words)
    return similarity_matrix

def sentence_similarity(sent1, sent2, stop_words=None):
    if stop_words is None:
        stop_words = set(stopwords.words('english'))
    words1 = [word.lower() for word in word_tokenize(sent1) if word.isalnum() and word.lower() not in stop_words]
    words2 = [word.lower() for word in word_tokenize(sent2) if word.isalnum() and word.lower() not in stop_words]
    all_words = list(set(words1 + words2))
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)
    for word in words1:
        vector1[all_words.index(word)] += 1
    for word in words2:
        vector2[all_words.index(word)] += 1
    return 1 - cosine_distance(vector1, vector2)

def textrank_summarize(text, num_sentences=3):
    sentences = sent_tokenize(text)
    stop_words = set(stopwords.words('english'))
    sentence_similarity_matrix = build_similarity_matrix(sentences, stop_words)
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_matrix)
    scores = nx.pagerank(sentence_similarity_graph)
    ranked_sentences = sorted(((scores[i], sentence) for i, sentence in enumerate(sentences)), reverse=True)
    summary = ' '.join([sentence for _, sentence in ranked_sentences[:num_sentences]])
    return summary

