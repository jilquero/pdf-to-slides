from typing import Dict
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

    content_renders = [render_content(content) for content in contents]

    bibliography_render = (
        bibliography_template.render(citations=citations) if citations else None
    )

    conclusion_render = conclusion_template.render(authors=authors)

    return document_template.render(
        title=title_render,
        contents=content_renders,
        bibliography=bibliography_render,
        conclusion=conclusion_render,
    )


def render_content(content: Dict) -> str:
    if "text" in content:
        return text_template.render(title=content["title"], text=content["text"])

    if "image" in content:
        return image_template.render(title=content["title"], image=content["image"])

    if "bullet_points" in content:
        return bullet_list_template.render(
            title=content["title"], bullet_points=content["bullet_points"]
        )

    if "table" in content:
        return table_template.render(title=content["title"], table=content["table"])
