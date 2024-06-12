import typer
import tempfile
import spacy
import en_core_web_sm  # noqa: F401
import pytextrank  # noqa: F401

from typing import Optional
from typing_extensions import Annotated
from .converters import pdf_to_markdown
from .converters import markdown_to_json
from .briefers import spacy_accurate_brief_en
from .briefers import nltk_accurate_brief_en
import nltk
from .briefers import bert_summarizer
from .briefers import bart_summarize
from .briefers import textrank_summarize

app = typer.Typer()


@app.callback()
def callback():
    """
    Pdf and markdown to slides converter
    """


@app.command()
def md(
    filename: Annotated[str, typer.Argument(help="PDF file to parse")],
    output: Annotated[str, typer.Argument(help="Output base folder path")] = "output",
    langs: Annotated[
        Optional[str], typer.Option(help="Languages to use for OCR, comma separated")
    ] = None,
    batch_multiplier: Annotated[
        int, typer.Option(help="How much to increase batch sizes")
    ] = 2,
    start_page: Annotated[
        Optional[int], typer.Option(help="Page to start processing at")
    ] = None,
    max_pages: Annotated[
        Optional[int], typer.Option(help="Maximum number of pages to parse")
    ] = None,
):
    """
    Convert pdf to markdown
    """
    langs = langs.split(",") if langs else None
    pdf_to_markdown(filename, output, langs, batch_multiplier, start_page, max_pages)


@app.command()
def json(filename: Annotated[str, typer.Argument(help="Markdown file to parse")]):
    """
    Convert markdown to json
    """
    markdown_to_json(filename)


@app.command()
def pdf_to_json(
    filename: Annotated[str, typer.Argument(help="Markdown file to parse")],
    langs: Annotated[
        Optional[str], typer.Option(help="Languages to use for OCR, comma separated")
    ] = None,
    batch_multiplier: Annotated[
        int, typer.Option(help="How much to increase batch sizes")
    ] = 2,
    start_page: Annotated[
        Optional[int], typer.Option(help="Page to start processing at")
    ] = None,
    max_pages: Annotated[
        Optional[int], typer.Option(help="Maximum number of pages to parse")
    ] = None,
):
    """
    Convert pdf to json
    """
    langs = langs.split(",") if langs else None
    with tempfile.TemporaryDirectory() as tempdir:
        path = pdf_to_markdown(filename, tempdir, langs, batch_multiplier, start_page, max_pages)
        markdown_to_json(f"{path}/{path.split("/")[-1]}.md")


@app.command()
def summarize():
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("textrank")

    example_text = """Celem ćwiczenia jest przedstawienie zaawansowanych metod klasyfikacji, szczególnie skupiając się na różnych strategiach i technikach przy użyciu biblioteki scikit-learn w języku Python. Poniżej znajduje się syntetyczny opis poszczególnych kroków w związku z realizacją Laboraotrium 1:
        1. Wczytanie i zbadanie zbioru danych MNIST, klasycznego zbioru danych w uczeniu maszynowym, zawierającego obrazy cyfr pisanych odręcznie. Przedstawiono typowe kroki występujące w projektach uczenia maszynowego i sztucznej inteligencji: wczytywanie danych, wizualizację, przetwarzanie wstępne oraz podział na zbiory treningowe i testowe.
        2. Stworzenie modeli klasyfikatorów binarnych, zaczynając od klasyfikatora Stochastic Gradient Descent (SGD). Omówiono i zademonstrowano różne miary wydajności, w tym dokładność, macierz pomyłek, precyzja, czułość oraz krzywa ROC, w celu oceny skuteczności klasyfikatora. Następnie przedstawiono uczenie wieloklasowe przy użyciu maszyn wektorów nośnych (SVM) oraz strategie OneVsRest.
        3. W drugiej części zagłębiamy się w bardziej skomplikowane scenariusze, takie jak klasyfikacja wieloetykietowa i wielowynikowa. Na przykład, używamy klasyfikatora K-Neighbors do obsługi wielu etykiet oraz klasyfikatora lasu losowego do klasyfikacji wielowynikowej, radząc sobie z bardziej zaawansowanymi scenariuszami. Przedstawiono praktyczne fragmenty kodu do tworzenia i interpretowania macierzy pomyłek, krzywych precyzja-odwołanie i krzywych ROC,zapewniając zrozumienie różnych metryk oceny.
        4. W instrukcji położono nacisk na wizualizację danych wraz z praktycznymi przykładami."""

    print('Original Document Size: ', len(example_text))
    doc = nlp(example_text)

    for sent in doc._.textrank.summary():
        print("Summary: ", sent)
        print('Summary Length:', len(sent))



@app.command()
def spacy_acc():
    # Example usage with an English text
    example_text_en = """The purpose of the exercise is to present advanced classification methods, specifically focusing on various strategies and techniques using the scikit-learn library in Python. The following is a synthetic description of the various steps in connection with the implementation of Laboraotrium 1:
     1. loading and examining the MNIST dataset, a classic dataset in machine learning that contains images of handwritten digits. The typical steps found in machine learning and artificial intelligence projects are presented: loading the data, visualization, preprocessing, and splitting it into training and test sets.
     2. creation of binary classifier models, starting with the Stochastic Gradient Descent (SGD) classifier. Various performance measures, including accuracy, confusion matrix, precision, sensitivity and ROC curve, were discussed and demonstrated to evaluate the classifier's performance. Multi-class learning using support vector machines (SVMs) and OneVsRest strategies are then presented.
     3. In the second part, we delve into more complicated scenarios, such as multi-label and multi-vendor classification. For example, we use the K-Neighbors classifier to handle multiple labels and the Random Forest classifier for multi-label classification, tackling more advanced scenarios. Practical code snippets are presented for creating and interpreting confusion matrices, precision-recall curves and ROC curves, providing an understanding of various evaluation metrics.
     4. The manual emphasizes data visualization with practical examples."""

    summary = spacy_accurate_brief_en(example_text_en, num_sentences=3)
    print(summary)


@app.command()
def nltk_sum():#[not too good] basic summarizer using sentence tokenization and scoring sentences based on word frequencies

    # Download necessary NLTK resources
    nltk.download('punkt')
    nltk.download('stopwords')
    # Example usage with an English text
    example_text_en = """The purpose of the exercise is to present advanced classification methods, specifically focusing on various strategies and techniques using the scikit-learn library in Python. The following is a synthetic description of the various steps in connection with the implementation of Laboraotrium 1:
     1. loading and examining the MNIST dataset, a classic dataset in machine learning that contains images of handwritten digits. The typical steps found in machine learning and artificial intelligence projects are presented: loading the data, visualization, preprocessing, and splitting it into training and test sets.
     2. creation of binary classifier models, starting with the Stochastic Gradient Descent (SGD) classifier. Various performance measures, including accuracy, confusion matrix, precision, sensitivity and ROC curve, were discussed and demonstrated to evaluate the classifier's performance. Multi-class learning using support vector machines (SVMs) and OneVsRest strategies are then presented.
     3. In the second part, we delve into more complicated scenarios, such as multi-label and multi-vendor classification. For example, we use the K-Neighbors classifier to handle multiple labels and the Random Forest classifier for multi-label classification, tackling more advanced scenarios. Practical code snippets are presented for creating and interpreting confusion matrices, precision-recall curves and ROC curves, providing an understanding of various evaluation metrics.
     4. The manual emphasizes data visualization with practical examples."""

    summary = nltk_accurate_brief_en(example_text_en, num_sentences=3)
    print(summary)


@app.command()
def bert_sum():#[long 7 min] extractive summarization, where sentences are ranked based on their importance and the top sentences form the summary

    # Example usage with an English text
    example_text_en = """The purpose of the exercise is to present advanced classification methods, specifically focusing on various strategies and techniques using the scikit-learn library in Python. The following is a synthetic description of the various steps in connection with the implementation of Laboraotrium 1:
     1. loading and examining the MNIST dataset, a classic dataset in machine learning that contains images of handwritten digits. The typical steps found in machine learning and artificial intelligence projects are presented: loading the data, visualization, preprocessing, and splitting it into training and test sets.
     2. creation of binary classifier models, starting with the Stochastic Gradient Descent (SGD) classifier. Various performance measures, including accuracy, confusion matrix, precision, sensitivity and ROC curve, were discussed and demonstrated to evaluate the classifier's performance. Multi-class learning using support vector machines (SVMs) and OneVsRest strategies are then presented.
     3. In the second part, we delve into more complicated scenarios, such as multi-label and multi-vendor classification. For example, we use the K-Neighbors classifier to handle multiple labels and the Random Forest classifier for multi-label classification, tackling more advanced scenarios. Practical code snippets are presented for creating and interpreting confusion matrices, precision-recall curves and ROC curves, providing an understanding of various evaluation metrics.
     4. The manual emphasizes data visualization with practical examples."""

    summary = bert_summarizer(example_text_en)
    #The purpose of the exercise is to present advanced classification methods, specifically focusing on various strategies and techniques using the scikit-learn library in Python. The typical steps found in machine learning and artificial intelligence projects are presented: loading the data, visualization, preprocessing, and splitting it into training and test sets. creation of binary classifier models, starting with the Stochastic Gradient Descent (SGD) classifier.
    print(summary)


@app.command()
def bart_sum():#[really long 10min] BART - abstractive summarization.

    # Example usage with an English text
    example_text_en = """The purpose of the exercise is to present advanced classification methods, specifically focusing on various strategies and techniques using the scikit-learn library in Python. The following is a synthetic description of the various steps in connection with the implementation of Laboraotrium 1:
     1. loading and examining the MNIST dataset, a classic dataset in machine learning that contains images of handwritten digits. The typical steps found in machine learning and artificial intelligence projects are presented: loading the data, visualization, preprocessing, and splitting it into training and test sets.
     2. creation of binary classifier models, starting with the Stochastic Gradient Descent (SGD) classifier. Various performance measures, including accuracy, confusion matrix, precision, sensitivity and ROC curve, were discussed and demonstrated to evaluate the classifier's performance. Multi-class learning using support vector machines (SVMs) and OneVsRest strategies are then presented.
     3. In the second part, we delve into more complicated scenarios, such as multi-label and multi-vendor classification. For example, we use the K-Neighbors classifier to handle multiple labels and the Random Forest classifier for multi-label classification, tackling more advanced scenarios. Practical code snippets are presented for creating and interpreting confusion matrices, precision-recall curves and ROC curves, providing an understanding of various evaluation metrics.
     4. The manual emphasizes data visualization with practical examples."""

    summary = bart_summarize(example_text_en)
    #he purpose of the exercise is to present advanced classification methods using the scikit-learn library in Python. The typical steps found in machine learning and artificial intelligence projects are presented. In the second part, we delve into more complicated scenarios, such as multi-label and multi-vendor classification.
    print(summary)


@app.command()
def txt_rank_sum():#really fast - really dirty garbage

    # Example usage with an English text
    example_text_en = """The purpose of the exercise is to present advanced classification methods, specifically focusing on various strategies and techniques using the scikit-learn library in Python. The following is a synthetic description of the various steps in connection with the implementation of Laboraotrium 1:
     1. loading and examining the MNIST dataset, a classic dataset in machine learning that contains images of handwritten digits. The typical steps found in machine learning and artificial intelligence projects are presented: loading the data, visualization, preprocessing, and splitting it into training and test sets.
     2. creation of binary classifier models, starting with the Stochastic Gradient Descent (SGD) classifier. Various performance measures, including accuracy, confusion matrix, precision, sensitivity and ROC curve, were discussed and demonstrated to evaluate the classifier's performance. Multi-class learning using support vector machines (SVMs) and OneVsRest strategies are then presented.
     3. In the second part, we delve into more complicated scenarios, such as multi-label and multi-vendor classification. For example, we use the K-Neighbors classifier to handle multiple labels and the Random Forest classifier for multi-label classification, tackling more advanced scenarios. Practical code snippets are presented for creating and interpreting confusion matrices, precision-recall curves and ROC curves, providing an understanding of various evaluation metrics.
     4. The manual emphasizes data visualization with practical examples."""

    summary = textrank_summarize(example_text_en)
    #For example, we use the K-Neighbors classifier to handle multiple labels and the Random Forest classifier for multi-label classification, tackling more advanced scenarios. The typical steps found in machine learning and artificial intelligence projects are presented: loading the data, visualization, preprocessing, and splitting it into training and test sets. The purpose of the exercise is to present advanced classification methods, specifically focusing on various strategies and techniques using the scikit-learn library in Python..
    print(summary)

