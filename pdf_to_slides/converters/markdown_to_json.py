import json

from markdown_to_json import jsonify


def markdown_to_json(filename: str) -> str:
    """
    Markdown to json converter
    """
    print("Converting markdown to json")

    with open(filename, "r") as f:
        markdown = f.read()

    markdown = jsonify(markdown)

    json_formatted_str = json.dumps(json.loads(markdown), indent=2)
    print(json_formatted_str)
    return json_formatted_str
