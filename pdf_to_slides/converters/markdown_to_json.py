import json

from markdown_to_json import jsonify


def markdown_to_json(markdown: str) -> str:
    """
    Markdown to json converter
    """
    markdown = jsonify(markdown)
    return json.dumps(json.loads(markdown), indent=2)
