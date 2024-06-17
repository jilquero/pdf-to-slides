from jinja2 import Environment, PackageLoader, select_autoescape
from babel.support import Translations

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
bullet_list_template = env.get_template("bullet_list.tex")
image_template = env.get_template("image.tex")
table_template = env.get_template("table.tex")
bibliography_template = env.get_template("bibliography.tex")
conclusion_template = env.get_template("conclusion.tex")
document_template = env.get_template("document.tex")


def data_to_latex(
    title: str,
    contents: list[dict[str, str]] = [],
    authors: list[dict[str, str]] = [],
    city: str = None,
    universities: list[dict[str, str]] = [],
    citations: list[dict[str, str]] = [],
) -> str:
    title_render = title_template.render(
        title=title,
        authors=authors,
        universities=universities,
        city=city,
    )

    content_renders = []
    for content in contents:
        if "text" in content:
            content_render = text_template.render(
                title=content["title"],
                text=content["text"],
            )
        elif "image" in content:
            content_render = image_template.render(
                title=content["title"],
                image=content["image"],
            )
        elif "bullet_points" in content:
            content_render = bullet_list_template.render(
                title=content["title"],
                bullet_points=content["bullet_points"],
            )
        elif "table" in content:
            content_render = table_template.render(
                title=content["title"],
                table=content["table"],
            )

        content_renders.append(content_render)

    bibliography_render = None
    if citations:
        bibliography_render = bibliography_template.render(citations=citations)

    conclusion_render = conclusion_template.render(authors=authors)

    return document_template.render(
        title=title_render,
        contents=content_renders,
        bibliography=bibliography_render,
        conclusion=conclusion_render,
    )
