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

def main(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    translated_data = translate_json(data)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(translated_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python translate_json.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    main(input_file, output_file)
