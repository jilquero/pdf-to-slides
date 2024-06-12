from pathlib import Path
from ..converters import pdf_to_markdown as pdf_to_markdown_converter


def pdf_to_markdown(
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
    langs = langs.split(",") if langs else None
    path = pdf_to_markdown_converter(
        filename, output, langs, batch_multiplier, start_page, max_pages
    )
    return path
