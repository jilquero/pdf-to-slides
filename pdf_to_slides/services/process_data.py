from . import summarize_text
from . import translate_text


def process_data(data: dict) -> dict:
    """
    Process data
    """
    data |= {
        "title": translate_text(data.get("title", "")),
        "contents": [process_content(x) for x in data.get("contents", [])],
    }
    return data


def process_content(content: dict) -> dict:
    """
    Process content
    """
    return {
        "title": translate_text(content.get("title", "")),
        "content": translate_text(summarize_text(content.get("content", ""))),
    }
