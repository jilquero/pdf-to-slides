import os
import sys
import typer
import tempfile
import json as json_module

from pprint import pprint
from pathlib import Path
from typing import Optional
from typing_extensions import Annotated
from contextlib import redirect_stdout

from .services import data_to_latex
from .services import pdf_to_markdown
from .services import markdown_to_dictionary
from .services import summarize_text
from .services import pdf_to_slides
from .services import process_data
from .converters import json_to_data as json_to_data_converter
from .converters import data_to_latex as data_to_latex_converter

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
        markdown = pdf_to_markdown(
            filename, output, langs, batch_multiplier, start_page, max_pages
        )

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
        path = pdf_to_markdown(
            filename, tempdir, langs, batch_multiplier, start_page, max_pages
        )
        markdown_file = os.path.join(path, f"{os.path.basename(path)}.md")
        dict_data = markdown_to_dictionary(markdown_file)

    json_output = json_module.dumps(dict_data, indent=2)
    print(json_output)


@app.command()
def summarize(
    text: Annotated[str, typer.Argument(help="Text to summarize")],
):
    with redirect_stdout(os.devnull):
        summary = summarize_text(text)

    print(summary)


@app.command()
def summarize_json(
    input_file: Annotated[Path, typer.Argument(help="JSON file to summarize")],
    output_file: Annotated[Path, typer.Argument(help="Output JSON file path")],
):
    """
    Summarize contents of a JSON file and output to another JSON file.
    """
    with open(input_file, "r", encoding="utf-8") as f:
        data = json_module.load(f)

    data = json_to_data_converter(data)
    summarized_data = process_data(data)

    with open(output_file, "w", encoding="utf-8") as f:
        json_module.dump(summarized_data, f, indent=2)

    print(f"Summarized JSON written to {output_file}")


@app.command()
def template():
    """
    Convert data to latex
    """
    with redirect_stdout(os.devnull):
        latex = data_to_latex()

    print(latex)


@app.command()
def json_to_data(
    filename: Annotated[Path, typer.Argument(help="JSON file to parse")],
):
    """
    Convert json to latex
    """
    with redirect_stdout(os.devnull):
        dictionary = json_module.load(open(filename, "r", encoding="utf-8"))
        data = json_to_data_converter(dictionary)
        data = process_data(data)

    pprint(data)


@app.command()
def json_to_latex(
    filename: Annotated[Path, typer.Argument(help="JSON file to parse")],
):
    """
    Convert json to latex
    """
    with redirect_stdout(os.devnull):
        dictionary = json_module.load(open(filename, "r", encoding="utf-8"))
        data = json_to_data_converter(dictionary)
        data = process_data(data)
        latex = data_to_latex_converter(data["title"], data["contents"])

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
        slides = pdf_to_slides(
            filename, output, langs, batch_multiplier, start_page, max_pages
        )

    print(slides)
