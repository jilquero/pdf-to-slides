import re
import os

from PIL import Image
from pathlib import Path
from typing import Dict, Tuple


def markdown_with_images(filename: Path) -> Tuple[str, Dict[str, Image.Image]]:
    with open(filename, "r", encoding="utf-8") as f:
        markdown = f.read()

    markdown_path = os.path.dirname(filename)
    images = re.findall(r"!\[.*\]\((.*)\)", markdown)
    images = {image: os.path.join(markdown_path, image) for image in images}
    images = {image: Image.open(path) for image, path in images.items()}

    return markdown, images
