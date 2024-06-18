import json
import sys
from googletrans import Translator

def translate_text(text, src='en', dest='pl'):
    translator = Translator()
    translation = translator.translate(text, src=src, dest=dest)
    return translation.text

def translate_json(input_json, src='en', dest='pl'):
    if isinstance(input_json, dict):
        return {key: translate_json(value, src, dest) for key, value in input_json.items()}
    elif isinstance(input_json, list):
        return [translate_json(element, src, dest) for element in input_json]
    elif isinstance(input_json, str):
        return translate_text(input_json, src, dest)
    else:
        return input_json
