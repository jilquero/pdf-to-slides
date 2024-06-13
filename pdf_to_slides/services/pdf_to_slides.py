import sys
import tempfile

from pathlib import Path
from contextlib import redirect_stdout

from ..converters import json_to_data as json_to_data_converter
from ..converters import data_to_latex as data_to_latex_converter

from . import pdf_to_markdown as pdf_to_markdown_service
from . import markdown_to_dictionary as markdown_to_dictionary_service
from . import summarize_text


def pdf_to_slides(
    filename: Path,
    output: str = "output",
    langs: list[str] = None,
    batch_multiplier: int = 2,
    start_page: int = None,
    max_pages: int = None,
) -> str:
    """
    Pdf and markdown to slides converter
    """
    with tempfile.TemporaryDirectory() as tempdir, redirect_stdout(sys.stderr):
        path = pdf_to_markdown_service(filename, tempdir, langs, batch_multiplier, start_page, max_pages)
        dictionary = markdown_to_dictionary_service(f"{path}/{path.split("/")[-1]}.md")
        data = json_to_data_converter(dictionary)
        data["contents"] = list(map(lambda x: x | {"content": summarize_text(x["content"])}, data.get("contents", [])))
        latex = data_to_latex_converter(data["title"], data["contents"])

    return latex