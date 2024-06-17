import inspect

from ..converters import data_to_latex as data_to_latex_converter


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
        {"name": "Jan Kowalski", "email": "j.kowalski@pl.edu.pl", "university_id": "1"},
        {"name": "Janina Nowak", "email": "j.nowak@pl.edu.pl", "university_id": "2"},
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
            "text": inspect.cleandoc(
                """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus. Suspendisse lectus tortor,
            dignissim sit amet, adipiscing nec, ultricies sed, dolor. Cras elementum ultrices diam. Maecenas ligula massa, varius a, semper congue,
            euismod non, mi. Proin porttitor, orci nec nonummy molestie, enim est eleifend mi, non fermentum diam nisl sit amet erat. Duis semper.
            Duis arcu massa, scelerisque vitae, consequat in, pretium a, enim. Pellentesque congue. Ut in risus volutpat libero pharetra tempor.
            Cras vestibulum bibendum augue. Praesent egestas leo in pede. Praesent blandit odio eu enim. Pellentesque sed dui ut augue blandit sodales."""
            ),
        },
        {"title": "Text title 2", "image": "example.png"},
        {
            "title": "Text title 3",
            "bullet_points": [
                "bullet 1",
                "bullet 2",
                "bullet 3",
            ],
        },
        {
            "title": "Text title 4",
            "table": {
                "header": ["Header 1", "Header 2", "Header 3"],
                "rows": [
                    ["Row 1, Column 1", "Row 1, Column 2", "Row 1, Column 3"],
                    ["Row 2, Column 1", "Row 2, Column 2", "Row 2, Column 3"],
                    ["Row 3, Column 1", "Row 3, Column 2", "Row 3, Column 3"],
                ],
            },
        },
    ]

    citations = [
        {
            "ref": "art1_Kowal2000",
            "citation": "Kowal, P.: Fuzzy Controller for Mechanical Systems. IEEE Transactions on Fuzzy Systems \textbf{8}, 645--652 (2000)",
        },
        {
            "ref": "book1_Silverman1986",
            "citation": "Silverman, B.W.: Density Estimation for Statistcs and Data Analysis, Chapman and Hall, London (1986)",
        },
        {
            "ref": "book2_Wandl1995",
            "citation": "Wand, M.P., Jones, M.C.: Kernal Smoothing, Chapman and Hall, London (1995)",
        },
        {
            "ref": "book3_Berger1980",
            "citation": "Berger, J.O.: Statistical Decision Theroy, Springer-Verlag, New York (1980)",
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
