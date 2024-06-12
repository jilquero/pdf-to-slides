import typer
import tempfile
import spacy
import inspect
import en_core_web_sm  # noqa: F401
import pytextrank  # noqa: F401

from typing import Optional
from typing_extensions import Annotated

from .converters import data_to_latex
from .converters import pdf_to_markdown
from .converters import markdown_to_json

app = typer.Typer()


@app.callback()
def callback():
    """
    Pdf and markdown to slides converter
    """


@app.command()
def md(
    filename: Annotated[str, typer.Argument(help="PDF file to parse")],
    output: Annotated[str, typer.Argument(help="Output base folder path")] = "output",
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
    langs = langs.split(",") if langs else None
    pdf_to_markdown(filename, output, langs, batch_multiplier, start_page, max_pages)


@app.command()
def json(filename: Annotated[str, typer.Argument(help="Markdown file to parse")]):
    """
    Convert markdown to json
    """
    markdown_to_json(filename)


@app.command()
def pdf_to_json(
    filename: Annotated[str, typer.Argument(help="Markdown file to parse")],
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
    langs = langs.split(",") if langs else None
    with tempfile.TemporaryDirectory() as tempdir:
        path = pdf_to_markdown(filename, tempdir, langs, batch_multiplier, start_page, max_pages)
        markdown_to_json(f"{path}/{path.split("/")[-1]}.md")


@app.command()
def summarize():
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("textrank")

    example_text = ""

    print('Original Document Size: ', len(example_text))
    doc = nlp(example_text)

    for sent in doc._.textrank.summary():
        print("Summary: ", sent)
        print('Summary Length:', len(sent))


@app.command()
def template():
    """
    Convert data to latex
    """
    title = "Hello, World!"
    authors = [
        {
            "name": "Jan Kowalski",
            "email": "j.kowalski@pl.edu.pl",
            "university": "1"
        },
        {
            "name": "Janina Nowak",
            "email": "j.nowak@pl.edu.pl",
            "university": "2"
        },
    ]
    universities = [
        {
            "name": "University of Technology, Warszawska 24, PL-31-155 Cracow, Poland",
            "id": "1",
        },
        {
            "name": "Catholic University of Lublin, Raclawickie 14, PL-20-950 Lublin, Poland",
            "id": "2",
        },
    ]
    city = "Lublin"

    contents = [
        {
            "title": "Text title 1",
            "content": inspect.cleandoc("""Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus. Suspendisse lectus tortor,
            dignissim sit amet, adipiscing nec, ultricies sed, dolor. Cras elementum ultrices diam. Maecenas ligula massa, varius a, semper congue,
            euismod non, mi. Proin porttitor, orci nec nonummy molestie, enim est eleifend mi, non fermentum diam nisl sit amet erat. Duis semper.
            Duis arcu massa, scelerisque vitae, consequat in, pretium a, enim. Pellentesque congue. Ut in risus volutpat libero pharetra tempor.
            Cras vestibulum bibendum augue. Praesent egestas leo in pede. Praesent blandit odio eu enim. Pellentesque sed dui ut augue blandit sodales."""),
        },
        {
            "title": "Text title 2",
            "content": inspect.cleandoc("""Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus. Suspendisse lectus tortor,
            dignissim sit amet, adipiscing nec, ultricies sed, dolor. Cras elementum ultrices diam. Maecenas ligula massa, varius a, semper congue,
            euismod non, mi. Proin porttitor, orci nec nonummy molestie, enim est eleifend mi, non fermentum diam nisl sit amet erat. Duis semper.
            Duis arcu massa, scelerisque vitae, consequat in, pretium a, enim. Pellentesque congue. Ut in risus volutpat libero pharetra tempor.
            Cras vestibulum bibendum augue. Praesent egestas leo in pede. Praesent blandit odio eu enim. Pellentesque sed dui ut augue blandit sodales."""),
        },
    ]

    citations = [
        {
            "ref": "art1_Kowal2000",
            "text": "Kowal, P.: Fuzzy Controller for Mechanical Systems. IEEE Transactions on Fuzzy Systems \textbf{8}, 645--652 (2000)",
        },
        {
            "ref": "book1_Silverman1986",
            "text": "Silverman, B.W.: Density Estimation for Statistcs and Data Analysis, Chapman and Hall, London (1986)",
        },
        {
            "ref": "book2_Wandl1995",
            "text": "Wand, M.P., Jones, M.C.: Kernal Smoothing, Chapman and Hall, London (1995)",
        },
        {
            "ref": "book3_Berger1980",
            "text": "Berger, J.O.: Statistical Decision Theroy, Springer-Verlag, New York (1980)",
        },
    ]

    latex = data_to_latex(
        title=title,
        contents=contents,
        authors=authors,
        universities=universities,
        city=city,
        citations=citations,
    )
    print(latex)
