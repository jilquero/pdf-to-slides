import typer
import tempfile
import spacy
from collections import Counter
from heapq import nlargest
import en_core_web_sm  # noqa: F401
import xx_sent_ud_sm
#import pytextrank  # noqa: F401
import PyPDF2
import os
from typing import Optional
from typing_extensions import Annotated
from .converters import pdf_to_markdown, markdown_to_json, markdown_to_latex
from .renderer import SlideRenderer

app = typer.Typer()

@app.callback()
def callback():
    """
    Pdf and markdown to slides converter
    """

@app.command()
def merge(
    pdf_files: Annotated[list[str], typer.Argument(help="List of PDF files to merge")],
    output_filename: Annotated[str, typer.Argument(help="Output PDF file name")],
):
    """
    Merge multiple PDF files into one.
    """
    pdf_merger = PyPDF2.PdfMerger()

    for pdf in pdf_files:
        if os.path.exists(pdf):
            pdf_merger.append(pdf)
        else:
            print(f"File {pdf} does not exist and will be skipped.")
    
    with open(output_filename, 'wb') as output_file:
        pdf_merger.write(output_file)
    print(f"Merged PDF saved as {output_filename}")


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
        markdown_to_json(f"{path}/{path.split('/')[-1]}.md")


@app.command()
def summarize():
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("textrank")

    example_text = ""

    print('Original Document Size: ', len(example_text))
    doc = nlp(example_text)

    for sent in doc._.textrank.summary():
        print("Summary: ", sent)
        print('Summary Length:', len(sent))


@app.command()
def streszczenie():
    # Wczytanie modelu językowego
    nlp = spacy.load('xx_sent_ud_sm')
    nlp_en = spacy.load('en_core_web_sm')

    # Odczytanie pliku Markdown
    with open('./output/list_motywacyjny_ŁukaszSendecki/list_motywacyjny_ŁukaszSendecki.md', 'r', encoding='utf-8') as file:
        markdown_content = file.read()

    example = """"""

    # Przetwarzanie tekstu za pomocą spaCy
    doc = nlp(markdown_content) #markdown_content

    # Tokenizacja i filtrowanie
    words = [token.text for token in doc if not token.is_stop and not token.is_punct]
    word_freq = Counter(words)

    # Ważność zdań
    sentence_scores = {}
    for sent in doc.sents:
        for word in sent:
            if word.text in word_freq:
                if sent not in sentence_scores:
                    sentence_scores[sent] = word_freq[word.text]
                else:
                    sentence_scores[sent] += word_freq[word.text]

    # Wybór najważniejszych zdań
    summary_length = 6 # Liczba zdań w streszczeniu
    summary_sentences = nlargest(summary_length, sentence_scores, key=sentence_scores.get)

    # Stworzenie streszczenia
    summary = ' '.join([sent.text for sent in summary_sentences])
    print(summary)

# TODO:
# there is no end{frame} after the last frame in document
# there are some "\\" in places where shouldn't be
# there is a problem with images which are not yet uploaded 

@app.command()
def convert_md_to_tex(
    md_file: str = typer.Argument(..., help="Path to the Markdown file to convert"),
    output_file: str = typer.Argument(..., help="Output LaTeX file name")
):
    """
    Convert a Markdown file to a LaTeX presentation.
    """
    markdown_to_latex.markdown_to_latex(md_file, output_file)
    typer.echo(f"Converted {md_file} to {output_file}")