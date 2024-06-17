# Text Summarization Models Performance

This document provides an overview of different NLP models used for text summarization, comparing their performance based on several criteria such as length of summary, number of sentences, readability, and generation speed (tested on i7 7gen, 16gb ram, integrated graphics).

## Summary of Results

| Command Name                                                    | Summary Length (chars from base 2494 into ...) | Number of Sentences in Summary     | Readability (1-3) | Generation Speed (min)                               |
| --------------------------------------------------------------- | ---------------------------------------------- | ---------------------------------- | ----------------- | ---------------------------------------------------- |
| spacy (target 3 sentences, no pipeline limit,transformer model) | 503                                            | 3                                  | 2                 | 18 seconds (pipeline optimalization -1 sec)          |
| spacy (target 3 sentences, no pipeline limit,average model)     | 503                                            | 3                                  | 3                 | 26 seconds                                           |
| spacy (target 3 sentences, no pipeline limit,small model)       | 503                                            | 3                                  | 2                 | 11 seconds                                           |
| nltk (word frequencies)                                         | 590                                            | 1(cherry icked sentemces)          | 1                 | 9 seconds (with downloading)                         |
| txt_rank (word frequencies)                                     | 588                                            | 0 (picked three central sentences) | 0                 | 10 seconds                                           |
| bert_sum                                                        | 655                                            | max 150 tokens                     | 3                 | 8 seconds (without downloading)                      |
| bart_sum                                                        | 314                                            | max 100 tokens                     | 3.02              | 40 seconds                                           |
| google (max_chunk_length = 1024,max_length=150, min_length=50 ) | 988                                            | max 100 tokens                     | 3                 | 2 minutes 10 seconds                                 |
| t5                                                              | 1588                                           | -                                  | 2.5               | 3 minutes 20 seconds (with downloading 8 min 30 sec) |

## Conclusion

From the above comparison, it is evident that the Spacy model is the best fit for summarizing text for presentations. It strikes a good balance between speed and accuracy, making it a reliable choice for generating summaries quickly without compromising on readability and coherence.
