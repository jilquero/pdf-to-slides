import inspect

from jinja2 import Environment, PackageLoader, select_autoescape
from babel.support import Translations

from ..converters import data_to_latex as data_to_latex_converter

env = Environment(
    loader=PackageLoader("pdf_to_slides", "../templates"),
    extensions=["jinja2.ext.i18n"],
    autoescape=select_autoescape(),
    trim_blocks=True,
    lstrip_blocks=True,
)
translations = Translations.load("locale", ["pl_PL"])
env.install_gettext_translations(translations)

title_template = env.get_template("title.tex")
text_template = env.get_template("text.tex")
bibliography_template = env.get_template("bibliography.tex")
conclusion_template = env.get_template("conclusion.tex")
document_template = env.get_template("document.tex")


def data_to_latex(
    title: str = "",
    contents: list[dict[str, str]] = [],
    authors: list[dict[str, str]] = [],
    city: str = None,
    universities: list[dict[str, str]] = [],
    citations: list[dict[str, str]] = [],
) -> str:
    title = "Hello, World!"
    authors = [
        {"name": "Jan Kowalski", "email": "j.kowalski@pl.edu.pl", "university": "1"},
        {"name": "Janina Nowak", "email": "j.nowak@pl.edu.pl", "university": "2"},
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
            "content": inspect.cleandoc(
                """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus. Suspendisse lectus tortor,
            dignissim sit amet, adipiscing nec, ultricies sed, dolor. Cras elementum ultrices diam. Maecenas ligula massa, varius a, semper congue,
            euismod non, mi. Proin porttitor, orci nec nonummy molestie, enim est eleifend mi, non fermentum diam nisl sit amet erat. Duis semper.
            Duis arcu massa, scelerisque vitae, consequat in, pretium a, enim. Pellentesque congue. Ut in risus volutpat libero pharetra tempor.
            Cras vestibulum bibendum augue. Praesent egestas leo in pede. Praesent blandit odio eu enim. Pellentesque sed dui ut augue blandit sodales."""
            ),
        },
        {
            "title": "Text title 2",
            "content": inspect.cleandoc(
                """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus. Suspendisse lectus tortor,
            dignissim sit amet, adipiscing nec, ultricies sed, dolor. Cras elementum ultrices diam. Maecenas ligula massa, varius a, semper congue,
            euismod non, mi. Proin porttitor, orci nec nonummy molestie, enim est eleifend mi, non fermentum diam nisl sit amet erat. Duis semper.
            Duis arcu massa, scelerisque vitae, consequat in, pretium a, enim. Pellentesque congue. Ut in risus volutpat libero pharetra tempor.
            Cras vestibulum bibendum augue. Praesent egestas leo in pede. Praesent blandit odio eu enim. Pellentesque sed dui ut augue blandit sodales."""
            ),
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

    latex = data_to_latex_converter(
        title=title,
        contents=contents,
        authors=authors,
        universities=universities,
        city=city,
        citations=citations,
    )

    return latex
