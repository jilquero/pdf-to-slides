def json_to_data(markdown_dict: dict) -> dict[str, str | list[dict[str, str]]]:
    """
    Json to data converter
    """
    contents = []
    for content in markdown_dict.values():
        for key, value in content.items():
            contents.append({"title": key, "text": value})

    data = {
        "title": list(markdown_dict.keys())[0],
        "contents": contents,
    }

    return data
