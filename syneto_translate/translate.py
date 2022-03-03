from googletrans import Translator


def translate_sentence(text: str, dest_lang: str) -> str:
    translator = Translator()
    result = translator.translate(text, dest=dest_lang)
    return result.text
