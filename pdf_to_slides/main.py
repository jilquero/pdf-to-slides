import typer
import tempfile
import spacy
import en_core_web_sm  # noqa: F401
import pytextrank  # noqa: F401

from typing import Optional
from typing_extensions import Annotated
from .converters import pdf_to_markdown
from .converters import markdown_to_json


# import for summarizers
import nltk

from .briefers import spacy_accurate_brief_en
from .briefers import spacy_tutorial
from .briefers import token_scorer

from .briefers import nltk_summarizer
from .briefers import bert_summarizer
from .briefers import bart_summarizer
from .briefers import textrank_summarizer


example_text_en = """Convolutional neural network (CNN) is a regularized type of feed-forward neural network that learns feature engineering by itself via filters (or kernel) optimization. Vanishing gradients and exploding gradients, seen during backpropagation in earlier neural networks, are prevented by using regularized weights over fewer connections. For example, for each neuron in the fully-connected layer, 10,000 weights would be required for processing an image sized 100 × 100 pixels. However, applying cascaded convolution (or cross-correlation) kernels, only 25 neurons are required to process 5x5-sized tiles. Higher-layer features are extracted from wider context windows, compared to lower-layer features. CNNs are also known as shift invariant or space invariant artificial neural networks (SIANN), based on the shared-weight architecture of the convolution kernels or filters that slide along input features and provide translation-equivariant responses known as feature maps. Counter-intuitively, most convolutional neural networks are not invariant to translation, due to the downsampling operation they apply to the input. Feed-forward neural networks are usually fully connected networks, that is, each neuron in one layer is connected to all neurons in the next layer. The "full connectivity" of these networks makes them prone to overfitting data. Typical ways of regularization, or preventing overfitting, include: penalizing parameters during training (such as weight decay) or trimming connectivity (skipped connections, dropout, etc.) Robust datasets also increase the probability that CNNs will learn the generalized principles that characterize a given dataset rather than the biases of a poorly-populated set. Convolutional networks were inspired by biological processes in that the connectivity pattern between neurons resembles the organization of the animal visual cortex. Individual cortical neurons respond to stimuli only in a restricted region of the visual field known as the receptive field. The receptive fields of different neurons partially overlap such that they cover the entire visual field. CNNs use relatively little pre-processing compared to other image classification algorithms. This means that the network learns to optimize the filters (or kernels) through automated learning, whereas in traditional algorithms these filters are hand-engineered. This independence from prior knowledge and human intervention in feature extraction is a major advantage."""


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
def spacy_sum():    #[currently the best]  --- 26 sec --- readibility 3/3 
    summary = spacy_accurate_brief_en(example_text_en, num_sentences=3)
    print(summary)


@app.command()
def bart_sum():     # --- 40 sec (+ model in first try) --- readibility 3.02/3
    summary = bart_summarizer(example_text_en)
    print(summary)


@app.command()
def bert_sum():     # --- 8 sec  (+ model in first try) --- readibility 3/3 
    summary = bert_summarizer(example_text_en)
    print(summary)


@app.command()
def nltk_sum():     # --- 9 sec --- readibility 1/3
    # Download necessary NLTK resources
    nltk.download('punkt')
    nltk.download('stopwords')
    summary = nltk_summarizer(example_text_en, num_sentences=3)
    print(summary)


@app.command()
def txt_rank_sum(): # --- 10 sec --- readibility 0/3
    summary = textrank_summarizer(example_text_en)
    print(summary)


@app.command()
def token_scorer_cmd(): # --- 13 sec --- returns:most connected synthantically tokens 
    summary = token_scorer(example_text_en)
    print(summary)


@app.command()  # [TMP] - for tests
def spacy_tutorial():
    summary = spacy_tutorial(example_text_en)
    print(summary)