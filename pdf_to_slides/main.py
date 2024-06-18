import os
import typer
import json as json_module

from pathlib import Path
from typing import Optional
from typing_extensions import Annotated

from .services import pdf_to_markdown
from .services import openai_api
from .services import data_to_latex
from .services import tex_to_pdf
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
    output: Annotated[
        Path, typer.Argument(help="Output base folder path")
    ] = "output.md",
    output_dir: Annotated[Path, typer.Option(help="Output directory path")] = "output",
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
    assert os.path.exists(filename), f"File {filename} does not exist"
    assert filename.name.endswith(".pdf"), f"File {filename} is not a PDF file"

    markdown, images, _ = pdf_to_markdown(
        filename, langs, batch_multiplier, start_page, max_pages
    )

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    path = os.path.join(output_dir, output)
    with open(path, "w", encoding="utf-8") as f:
        f.write(markdown)

    for filename, image in images.items():
        path = os.path.join(output_dir, filename)
        image.save(path, "PNG")


@app.command()
def json(
    filename: Annotated[Path, typer.Argument(help="Markdown file to parse")],
    output: Annotated[
        Path, typer.Argument(help="Output base folder path")
    ] = "output.json",
):
    """
    Convert markdown to json
    """
    assert os.path.exists(filename), f"File {filename} does not exist"
    assert filename.name.endswith(".md"), f"File {filename} is not a markdown file"

    with open(filename, "r", encoding="utf-8") as f:
        markdown = f.read()

    data = openai_api(markdown)

    with open(output, "w", encoding="utf-8") as f:
        f.write(data)


@app.command()
def latex(
    filename: Annotated[Path, typer.Argument(help="Markdown file to parse")],
    output: Annotated[
        Path, typer.Argument(help="Output base folder path")
    ] = "output.tex",
):
    """
    Convert json to latex
    """
    assert os.path.exists(filename), f"File {filename} does not exist"
    assert filename.name.endswith(".json"), f"File {filename} is not a json file"

    with open(filename, "r", encoding="utf-8") as f:
        json = f.read()

    data = json_module.loads(json)
    latex = data_to_latex(
        data.get("title", ""),
        data.get("contents", []),
        data.get("authors", []),
        data.get("city", None),
        data.get("universities", []),
        data.get("bibliography", []),
    )

    with open(output, "w", encoding="utf-8") as f:
        f.write(latex)


@app.command()
def pdf(
    filename: Annotated[Path, typer.Argument(help="Markdown file to parse")],
    output: Annotated[
        Path, typer.Argument(help="Output base folder path")
    ] = "output.pdf",
):
    """
    Convert latex to pdf
    """
    assert os.path.exists(filename), f"File {filename} does not exist"
    assert filename.name.endswith(".tex"), f"File {filename} is not a tex file"

    with open(filename, "r", encoding="utf-8") as f:
        latex = f.read()

    pdf = tex_to_pdf(latex)

    with open(output, "wb") as f:
        f.write(pdf)


@app.command()
def convert(
    filename: Annotated[Path, typer.Argument(help="PDF file to parse")],
    output: Annotated[
        Path, typer.Argument(help="Output base folder path")
    ] = "output.tex",
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
    Convert pdf and markdown files to slides
    """
    assert os.path.exists(filename), f"File {filename} does not exist"
    assert any(
        filename.name.endswith(ext) for ext in [".pdf", ".md"]
    ), f"File {filename} is not a PDF or markdown file"

    langs = langs.split(",") if langs else None
    pdf = pdf_to_slides(filename, langs, batch_multiplier, start_page, max_pages)

    with open(output, "wb") as f:
        f.write(pdf)
