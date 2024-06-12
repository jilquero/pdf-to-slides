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
from .briefers import spacy_tutorial
from .briefers import token_scorer

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
def token_scorer():
    # Example usage with an English text
    example_text_en = """The purpose of the exercise is to present advanced classification methods, specifically focusing on various strategies and techniques using the scikit-learn library in Python. The following is a synthetic description of the various steps in connection with the implementation of Laboraotrium 1:
     1. loading and examining the MNIST dataset, a classic dataset in machine learning that contains images of handwritten digits. The typical steps found in machine learning and artificial intelligence projects are presented: loading the data, visualization, preprocessing, and splitting it into training and test sets.
     2. creation of binary classifier models, starting with the Stochastic Gradient Descent (SGD) classifier. Various performance measures, including accuracy, confusion matrix, precision, sensitivity and ROC curve, were discussed and demonstrated to evaluate the classifier's performance. Multi-class learning using support vector machines (SVMs) and OneVsRest strategies are then presented.
     3. In the second part, we delve into more complicated scenarios, such as multi-label and multi-vendor classification. For example, we use the K-Neighbors classifier to handle multiple labels and the Random Forest classifier for multi-label classification, tackling more advanced scenarios. Practical code snippets are presented for creating and interpreting confusion matrices, precision-recall curves and ROC curves, providing an understanding of various evaluation metrics.
     4. The manual emphasizes data visualization with practical examples."""

    summary = token_scorer(example_text_en)
    print(summary)

@app.command()
def sent():
    # Example usage with an English text
    example_text_en = """The purpose of the exercise is to present advanced classification methods, specifically focusing on various strategies and techniques using the scikit-learn library in Python. The following is a synthetic description of the various steps in connection with the implementation of Laboraotrium 1:
     1. loading and examining the MNIST dataset, a classic dataset in machine learning that contains images of handwritten digits. The typical steps found in machine learning and artificial intelligence projects are presented: loading the data, visualization, preprocessing, and splitting it into training and test sets.
     2. creation of binary classifier models, starting with the Stochastic Gradient Descent (SGD) classifier. Various performance measures, including accuracy, confusion matrix, precision, sensitivity and ROC curve, were discussed and demonstrated to evaluate the classifier's performance. Multi-class learning using support vector machines (SVMs) and OneVsRest strategies are then presented.
     3. In the second part, we delve into more complicated scenarios, such as multi-label and multi-vendor classification. For example, we use the K-Neighbors classifier to handle multiple labels and the Random Forest classifier for multi-label classification, tackling more advanced scenarios. Practical code snippets are presented for creating and interpreting confusion matrices, precision-recall curves and ROC curves, providing an understanding of various evaluation metrics.
     4. The manual emphasizes data visualization with practical examples."""

    summary = ultimate_sentence_scorer(example_text_en)
    print(summary)



@app.command()
def ultimate_brief():
    # Example usage with an English text
    example_text_en = """Convolutional neural network (CNN) is a regularized type of feed-forward neural network that learns feature engineering by itself via filters (or kernel) optimization. Vanishing gradients and exploding gradients, seen during backpropagation in earlier neural networks, are prevented by using regularized weights over fewer connections. For example, for each neuron in the fully-connected layer, 10,000 weights would be required for processing an image sized 100 × 100 pixels. However, applying cascaded convolution (or cross-correlation) kernels, only 25 neurons are required to process 5x5-sized tiles. Higher-layer features are extracted from wider context windows, compared to lower-layer features. CNNs are also known as shift invariant or space invariant artificial neural networks (SIANN), based on the shared-weight architecture of the convolution kernels or filters that slide along input features and provide translation-equivariant responses known as feature maps. Counter-intuitively, most convolutional neural networks are not invariant to translation, due to the downsampling operation they apply to the input. Feed-forward neural networks are usually fully connected networks, that is, each neuron in one layer is connected to all neurons in the next layer. The "full connectivity" of these networks makes them prone to overfitting data. Typical ways of regularization, or preventing overfitting, include: penalizing parameters during training (such as weight decay) or trimming connectivity (skipped connections, dropout, etc.) Robust datasets also increase the probability that CNNs will learn the generalized principles that characterize a given dataset rather than the biases of a poorly-populated set. Convolutional networks were inspired by biological processes in that the connectivity pattern between neurons resembles the organization of the animal visual cortex. Individual cortical neurons respond to stimuli only in a restricted region of the visual field known as the receptive field. The receptive fields of different neurons partially overlap such that they cover the entire visual field. CNNs use relatively little pre-processing compared to other image classification algorithms. This means that the network learns to optimize the filters (or kernels) through automated learning, whereas in traditional algorithms these filters are hand-engineered. This independence from prior knowledge and human intervention in feature extraction is a major advantage.
"""

    summary = spacy_accurate_brief_en(example_text_en, num_sentences=3)
    print(summary)

@app.command()
def spacy_tutorial():
    # ESpacy configured accordingly to the tutorial
    example_text_en = """The purpose of the exercise is to present advanced classification methods, specifically focusing on various strategies and techniques using the scikit-learn library in Python. The following is a synthetic description of the various steps in connection with the implementation of Laboraotrium 1:
     1. loading and examining the MNIST dataset, a classic dataset in machine learning that contains images of handwritten digits. The typical steps found in machine learning and artificial intelligence projects are presented: loading the data, visualization, preprocessing, and splitting it into training and test sets.
     2. creation of binary classifier models, starting with the Stochastic Gradient Descent (SGD) classifier. Various performance measures, including accuracy, confusion matrix, precision, sensitivity and ROC curve, were discussed and demonstrated to evaluate the classifier's performance. Multi-class learning using support vector machines (SVMs) and OneVsRest strategies are then presented.
     3. In the second part, we delve into more complicated scenarios, such as multi-label and multi-vendor classification. For example, we use the K-Neighbors classifier to handle multiple labels and the Random Forest classifier for multi-label classification, tackling more advanced scenarios. Practical code snippets are presented for creating and interpreting confusion matrices, precision-recall curves and ROC curves, providing an understanding of various evaluation metrics.
     4. The manual emphasizes data visualization with practical examples."""

    summary = spacy_tutorial(example_text_en)
    print(summary)

@app.command()
def nltk_sum():#[not too good] basic summarizer using sentence tokenization and scoring sentences based on word frequencies

    # Download necessary NLTK resources
    nltk.download('punkt')
    nltk.download('stopwords')
    # Example usage with an English text
    example_text_en = """Convolutional neural network (CNN) is a regularized type of feed-forward neural network that learns feature engineering by itself via filters (or kernel) optimization. Vanishing gradients and exploding gradients, seen during backpropagation in earlier neural networks, are prevented by using regularized weights over fewer connections. For example, for each neuron in the fully-connected layer, 10,000 weights would be required for processing an image sized 100 × 100 pixels. However, applying cascaded convolution (or cross-correlation) kernels, only 25 neurons are required to process 5x5-sized tiles. Higher-layer features are extracted from wider context windows, compared to lower-layer features. CNNs are also known as shift invariant or space invariant artificial neural networks (SIANN), based on the shared-weight architecture of the convolution kernels or filters that slide along input features and provide translation-equivariant responses known as feature maps. Counter-intuitively, most convolutional neural networks are not invariant to translation, due to the downsampling operation they apply to the input. Feed-forward neural networks are usually fully connected networks, that is, each neuron in one layer is connected to all neurons in the next layer. The "full connectivity" of these networks makes them prone to overfitting data. Typical ways of regularization, or preventing overfitting, include: penalizing parameters during training (such as weight decay) or trimming connectivity (skipped connections, dropout, etc.) Robust datasets also increase the probability that CNNs will learn the generalized principles that characterize a given dataset rather than the biases of a poorly-populated set. Convolutional networks were inspired by biological processes in that the connectivity pattern between neurons resembles the organization of the animal visual cortex. Individual cortical neurons respond to stimuli only in a restricted region of the visual field known as the receptive field. The receptive fields of different neurons partially overlap such that they cover the entire visual field. CNNs use relatively little pre-processing compared to other image classification algorithms. This means that the network learns to optimize the filters (or kernels) through automated learning, whereas in traditional algorithms these filters are hand-engineered. This independence from prior knowledge and human intervention in feature extraction is a major advantage.
"""

    summary = nltk_accurate_brief_en(example_text_en, num_sentences=3)
    print(summary)


@app.command()
def bert_sum():#[long 7 min] extractive summarization, where sentences are ranked based on their importance and the top sentences form the summary

    # Example usage with an English text
    example_text_en = """Convolutional neural network (CNN) is a regularized type of feed-forward neural network that learns feature engineering by itself via filters (or kernel) optimization. Vanishing gradients and exploding gradients, seen during backpropagation in earlier neural networks, are prevented by using regularized weights over fewer connections. For example, for each neuron in the fully-connected layer, 10,000 weights would be required for processing an image sized 100 × 100 pixels. However, applying cascaded convolution (or cross-correlation) kernels, only 25 neurons are required to process 5x5-sized tiles. Higher-layer features are extracted from wider context windows, compared to lower-layer features. CNNs are also known as shift invariant or space invariant artificial neural networks (SIANN), based on the shared-weight architecture of the convolution kernels or filters that slide along input features and provide translation-equivariant responses known as feature maps. Counter-intuitively, most convolutional neural networks are not invariant to translation, due to the downsampling operation they apply to the input. Feed-forward neural networks are usually fully connected networks, that is, each neuron in one layer is connected to all neurons in the next layer. The "full connectivity" of these networks makes them prone to overfitting data. Typical ways of regularization, or preventing overfitting, include: penalizing parameters during training (such as weight decay) or trimming connectivity (skipped connections, dropout, etc.) Robust datasets also increase the probability that CNNs will learn the generalized principles that characterize a given dataset rather than the biases of a poorly-populated set. Convolutional networks were inspired by biological processes in that the connectivity pattern between neurons resembles the organization of the animal visual cortex. Individual cortical neurons respond to stimuli only in a restricted region of the visual field known as the receptive field. The receptive fields of different neurons partially overlap such that they cover the entire visual field. CNNs use relatively little pre-processing compared to other image classification algorithms. This means that the network learns to optimize the filters (or kernels) through automated learning, whereas in traditional algorithms these filters are hand-engineered. This independence from prior knowledge and human intervention in feature extraction is a major advantage.
"""


    summary = bert_summarizer(example_text_en)
    #The purpose of the exercise is to present advanced classification methods, specifically focusing on various strategies and techniques using the scikit-learn library in Python. The typical steps found in machine learning and artificial intelligence projects are presented: loading the data, visualization, preprocessing, and splitting it into training and test sets. creation of binary classifier models, starting with the Stochastic Gradient Descent (SGD) classifier.
    print(summary)


@app.command()
def bart_sum():#[really long 10min] BART - abstractive summarization.

    # Example usage with an English text
    example_text_en = """Convolutional neural network (CNN) is a regularized type of feed-forward neural network that learns feature engineering by itself via filters (or kernel) optimization. Vanishing gradients and exploding gradients, seen during backpropagation in earlier neural networks, are prevented by using regularized weights over fewer connections. For example, for each neuron in the fully-connected layer, 10,000 weights would be required for processing an image sized 100 × 100 pixels. However, applying cascaded convolution (or cross-correlation) kernels, only 25 neurons are required to process 5x5-sized tiles. Higher-layer features are extracted from wider context windows, compared to lower-layer features. CNNs are also known as shift invariant or space invariant artificial neural networks (SIANN), based on the shared-weight architecture of the convolution kernels or filters that slide along input features and provide translation-equivariant responses known as feature maps. Counter-intuitively, most convolutional neural networks are not invariant to translation, due to the downsampling operation they apply to the input. Feed-forward neural networks are usually fully connected networks, that is, each neuron in one layer is connected to all neurons in the next layer. The "full connectivity" of these networks makes them prone to overfitting data. Typical ways of regularization, or preventing overfitting, include: penalizing parameters during training (such as weight decay) or trimming connectivity (skipped connections, dropout, etc.) Robust datasets also increase the probability that CNNs will learn the generalized principles that characterize a given dataset rather than the biases of a poorly-populated set. Convolutional networks were inspired by biological processes in that the connectivity pattern between neurons resembles the organization of the animal visual cortex. Individual cortical neurons respond to stimuli only in a restricted region of the visual field known as the receptive field. The receptive fields of different neurons partially overlap such that they cover the entire visual field. CNNs use relatively little pre-processing compared to other image classification algorithms. This means that the network learns to optimize the filters (or kernels) through automated learning, whereas in traditional algorithms these filters are hand-engineered. This independence from prior knowledge and human intervention in feature extraction is a major advantage.
"""

    summary = bart_summarize(example_text_en)
    #he purpose of the exercise is to present advanced classification methods using the scikit-learn library in Python. The typical steps found in machine learning and artificial intelligence projects are presented. In the second part, we delve into more complicated scenarios, such as multi-label and multi-vendor classification.
    print(summary)


@app.command()
def txt_rank_sum():#really fast - really dirty garbage

    # Example usage with an English text
    example_text_en = """Convolutional neural network (CNN) is a regularized type of feed-forward neural network that learns feature engineering by itself via filters (or kernel) optimization. Vanishing gradients and exploding gradients, seen during backpropagation in earlier neural networks, are prevented by using regularized weights over fewer connections. For example, for each neuron in the fully-connected layer, 10,000 weights would be required for processing an image sized 100 × 100 pixels. However, applying cascaded convolution (or cross-correlation) kernels, only 25 neurons are required to process 5x5-sized tiles. Higher-layer features are extracted from wider context windows, compared to lower-layer features. CNNs are also known as shift invariant or space invariant artificial neural networks (SIANN), based on the shared-weight architecture of the convolution kernels or filters that slide along input features and provide translation-equivariant responses known as feature maps. Counter-intuitively, most convolutional neural networks are not invariant to translation, due to the downsampling operation they apply to the input. Feed-forward neural networks are usually fully connected networks, that is, each neuron in one layer is connected to all neurons in the next layer. The "full connectivity" of these networks makes them prone to overfitting data. Typical ways of regularization, or preventing overfitting, include: penalizing parameters during training (such as weight decay) or trimming connectivity (skipped connections, dropout, etc.) Robust datasets also increase the probability that CNNs will learn the generalized principles that characterize a given dataset rather than the biases of a poorly-populated set. Convolutional networks were inspired by biological processes in that the connectivity pattern between neurons resembles the organization of the animal visual cortex. Individual cortical neurons respond to stimuli only in a restricted region of the visual field known as the receptive field. The receptive fields of different neurons partially overlap such that they cover the entire visual field. CNNs use relatively little pre-processing compared to other image classification algorithms. This means that the network learns to optimize the filters (or kernels) through automated learning, whereas in traditional algorithms these filters are hand-engineered. This independence from prior knowledge and human intervention in feature extraction is a major advantage.
"""

    summary = textrank_summarize(example_text_en)
    #For example, we use the K-Neighbors classifier to handle multiple labels and the Random Forest classifier for multi-label classification, tackling more advanced scenarios. The typical steps found in machine learning and artificial intelligence projects are presented: loading the data, visualization, preprocessing, and splitting it into training and test sets. The purpose of the exercise is to present advanced classification methods, specifically focusing on various strategies and techniques using the scikit-learn library in Python..
    print(summary)

