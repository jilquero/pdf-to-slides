from googletrans import Translator


def translate_text(text, src="en", dest="pl"):
    translator = Translator()
    translation = translator.translate(text, src=src, dest=dest)
    return translation.text
