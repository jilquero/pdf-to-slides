from PIL import Image
from pathlib import Path
from typing import Dict, Tuple
from marker.convert import convert_single_pdf
from marker.models import load_all_models


def pdf_to_markdown(
    filename: Path,
    langs: list[str] = None,
    batch_multiplier: int = 2,
    start_page: int = None,
    max_pages: int = None,
) -> Tuple[str, Dict[str, Image.Image]]:

    model_lst = load_all_models()
    full_text, images, _ = convert_single_pdf(
        filename,
        model_lst,
        max_pages=max_pages,
        langs=langs,
        batch_multiplier=batch_multiplier,
        start_page=start_page,
    )

    return full_text, images
