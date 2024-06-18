import json

from pathlib import Path
from typing import BinaryIO

from . import pdf_to_markdown
from . import markdown_with_images
from . import openai_api
from . import data_to_latex
from . import tex_to_pdf


def pdf_to_slides(
    filename: Path,
    langs: list[str] = None,
    batch_multiplier: int = 2,
    start_page: int = None,
    max_pages: int = None,
) -> BinaryIO:
    langs = langs.split(",") if langs else None

    markdown, images = (
        pdf_to_markdown(filename, langs, batch_multiplier, start_page, max_pages)
        if filename.suffix == ".pdf"
        else markdown_with_images(filename)
    )

    data = openai_api(markdown)

    data = json.loads(data)
    latex = data_to_latex(
        data.get("title", ""),
        data.get("contents", []),
        data.get("authors", []),
        data.get("city", None),
        data.get("universities", []),
        data.get("bibliography", []),
    )
    pdf = tex_to_pdf(latex, images)

    return pdf
