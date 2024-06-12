from ..converters import markdown_to_json as markdown_to_json_converter


def markdown_to_json(markdown: str) -> str:
    """
    Markdown to json converter
    """

    with open(markdown, "r") as f:
        markdown = f.read()
        md = markdown_to_json_converter(markdown)

    return md
