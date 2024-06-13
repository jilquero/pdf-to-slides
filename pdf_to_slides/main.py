import os
import sys
import typer
import tempfile
import json as json_module

from pathlib import Path
from typing import Optional
from typing_extensions import Annotated
from contextlib import redirect_stdout

from .services import data_to_latex
from .services import pdf_to_markdown
from .services import markdown_to_dictionary
from .services import summarize_text
from .services import pdf_to_slides

app = typer.Typer()


@app.callback()
def callback():
    """
    Pdf and markdown to slides converter
    """


@app.command()
def md(
    filename: Annotated[Path, typer.Argument(help="PDF file to parse")],
    output: Annotated[Path, typer.Argument(help="Output base folder path")] = "output",
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
    with redirect_stdout(os.devnull):
        markdown = pdf_to_markdown(filename, output, langs, batch_multiplier, start_page, max_pages)

    print(markdown)


@app.command()
def json(filename: Annotated[Path, typer.Argument(help="Markdown file to parse")]):
    """
    Convert markdown to json
    """
    with redirect_stdout(os.devnull):
        dict = markdown_to_dictionary(filename)

    print(json_module.dump(json_module.load(dict), indent=2))


@app.command()
def pdf_to_json(
    filename: Annotated[Path, typer.Argument(help="Markdown file to parse")],
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
    with tempfile.TemporaryDirectory() as tempdir, redirect_stdout(sys.stderr):
        path = pdf_to_markdown(filename, tempdir, langs, batch_multiplier, start_page, max_pages)
        dict = markdown_to_dictionary(f"{path}/{path.split("/")[-1]}.md")

    print(json_module.dump(json_module.load(dict), indent=2))


@app.command()
def summarize(text: Annotated[str, typer.Argument(help="Text to summarize")],):
    with redirect_stdout(os.devnull):
        summary = summarize_text(text)

    print(summary)


@app.command()
def template():
    """
    Convert data to latex
    """
    with redirect_stdout(os.devnull):
        latex = data_to_latex()

    print(latex)


@app.command()
def convert(
    filename: Annotated[Path, typer.Argument(help="PDF file to parse")],
    output: Annotated[Path, typer.Argument(help="Output base folder path")] = "output",
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
    with redirect_stdout(os.devnull):
        slides = pdf_to_slides(filename, output, langs, batch_multiplier, start_page, max_pages)

    print(slides)
