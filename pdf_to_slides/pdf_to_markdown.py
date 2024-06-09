import os

from marker.convert import convert_single_pdf
from marker.models import load_all_models
from marker.output import save_markdown


def pdf_to_markdown(
    filename: str,
    output: str = "output",
    langs: list[str] = None,
    batch_multiplier: int = 2,
    start_page: int = None,
    max_pages: int = None,
):
    """
    Pdf and markdown to slides converter
    """
    print("Loading models")

    model_lst = load_all_models()
    full_text, images, out_meta = convert_single_pdf(
        filename,
        model_lst,
        max_pages=max_pages,
        langs=langs,
        batch_multiplier=batch_multiplier,
        start_page=start_page,
    )

    filename = os.path.basename(filename)
    path = save_markdown(output, filename, full_text, images, out_meta)

    print(f"Saved markdown to the {path} folder")
