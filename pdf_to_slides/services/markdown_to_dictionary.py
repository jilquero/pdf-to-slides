from markdown_to_json import dictify


def markdown_to_dictionary(markdown: str):
    """
    Markdown to dictionary converter
    """

    with open(markdown, "r") as f:
        markdown = f.read()
        md = dictify(markdown)

    return md
