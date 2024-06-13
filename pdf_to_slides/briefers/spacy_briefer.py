import spacy
import pytextrank
from spacy.language import Language
from numpy import dot
from numpy.linalg import norm

def spacy_accurate_brief_en(text: str=None, num_sentences: int = 3) -> str:
    if text is None:
        return ""

    nlp = spacy.load("en_core_web_md",disable=['ner'])#en_core_web_trf

    #nlp.remove_pipe('ner') 
    nlp.add_pipe("textrank")

    print(nlp.pipe_names)

    doc = nlp(text) # Process the text

    # Extract the most important sentences using pytextrank
    summary_sentences = []
    for sent in doc._.textrank.summary(limit_sentences=num_sentences):
        summary_sentences.append(sent.text)
    
    result = ' '.join(summary_sentences)
    return result


def spacy_tutorial(text: str=None) -> str:  # TMP - [temporary function to work with spacy tutorial]
    nlp = spacy.load("en_core_web_sm")#en_core_web_md <-- średniej wielości model (mają wektory słów)
    #en_core_web_tr <-- model transformatora jest uczony całkowicie inaczej niż mały czy średni model
    doc = nlp(text)
    
    
    #for sent in doc.sents: #pojedyncze zdania
    #    print(sent)
    
    #for token in doc[:10]:
    #    print(token)

    sentence2=list(doc.sents)[1]
    
    token2=sentence2[2]
    print(token2)

    print(token2.text)
    print(token2.left_edge)
    print(token2.right_edge)
    print(token2.ent_type_)


    print(token2.lang_)#<--wskazanie języka słowa 'en'
    
    #małe modele "en_core_web_sm" mają skłonność do słabszego wykrywania granic zdań oraz klasyfikacji typów tokenów

    #word-to-vect jest starym (gorszym) sposobem niż spacy
    
    #Można sprawdzać jak ciągi tekstów semantycznie są do siebie podobne za pomocą "doc1.similarity(doc2)"
    # doc1 = nlp("jakiś tekst1"), doc2 = nlp("jakiś tekst2")
    #^ w taki sposób możemy sobie grupować tematycznie dokumenty, żeby tematyka była ciągła (wtedy po sobie układamy dokumenty o największej wartości podobieństwa)
    #https://youtu.be/dIUTsFT2MeQ?t=3866

    #Stworzenie nowego pustego "pipeline"
    nlp = spacy.blank("en") #<-- dodanie pustego pipe dla języka angielskiego
    nlp.add_pipe("sentencizer") #<-- tworzy pipeline, które ma sekwencję dwóch różnych rur (pipes)

        # Często warto użyć większego modelu, bo jest trenowany na większych danych i zawiera mniej typów różnych rur (pipe'ów)
        # coś może długi czas zajmować (47 minut)  na małym a 7 sekund na dużym

    #Dobrą alternatywą dla sprawdzenia jest stworzenie pustego modelu i dodanie pojedynczego pipe do niego (czasem jest szybsze niż na małych modelach) --- choć generuje mało dokładne wyniki

    return ""


# token scorer - scoring tokens between each other for most synthentically, thought that will essence the sentence, but it prints out the most connected  words (the words that most connected to each other)  
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
            filtered_tokens.extend([token for token, score in sorted_tokens if score >= threshold])

        # Create a new document with the filtered tokens
        doc = spacy.tokens.Doc(nlp.vocab, words=[token.text for token in filtered_tokens])
        return doc
    
    nlp.add_pipe("similarity_checker", last=True)

    doc = nlp(text)

    result = [token.text for token in doc]
    return result
