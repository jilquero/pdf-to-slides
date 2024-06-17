from . import summarize_text


def process_data(data: dict) -> dict:
    """
    Process data
    """
    return {
        "title": data.get("title", ""),
        "contents": [process_content(x) for x in data.get("contents", [])],
    }


def process_content(content: dict) -> dict:
    """
    Process content
    """
    return {
        "title": content.get("title", ""),
        "content": summarize_text(content.get("content", "")),
    }
