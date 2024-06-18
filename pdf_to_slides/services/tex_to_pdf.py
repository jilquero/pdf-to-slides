import os
import shutil
import tempfile
import subprocess

from PIL import Image
from typing import BinaryIO, Dict


def tex_to_pdf(latex: str, images: Dict[str, Image.Image] = {}) -> BinaryIO:
    pdflatex_path = shutil.which("pdflatex")
    if pdflatex_path is None:
        raise FileNotFoundError("pdflatex executable not found in system PATH")

    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            tex_file_path = os.path.join(temp_dir, "document.tex")
            with open(tex_file_path, "w", encoding="utf-8") as f:
                f.write(latex)

            for filename, image in images.items():
                image_path = os.path.join(temp_dir, filename)
                image.save(image_path, "PNG")

            args = [
                pdflatex_path,
                "-output-directory=" + temp_dir,
                "document.tex",
                "document.pdf",
            ]
            subprocess.run(args, check=True)
            subprocess.run(args, check=True)

            pdf_file_path = os.path.join(temp_dir, "document.pdf")
            with open(pdf_file_path, "rb") as f:
                return f.read()

        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")
