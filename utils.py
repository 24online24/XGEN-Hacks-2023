from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem
from azure.core.exceptions import HttpResponseError

from dotenv import load_dotenv
import os


def create_translator() -> TextTranslationClient:
    """Creează un client pentru serviciul de traducere de text de la Microsoft Azure."""
    load_dotenv()
    key = os.getenv("MSKEY")
    endpoint = os.getenv("ENDPOINT")
    region = os.getenv("REGION")

    credential = TranslatorCredential(key, region)
    return TextTranslationClient(
        endpoint=endpoint, credential=credential)


def translate_message(translator: TextTranslationClient, message: str, from_lang: str, to_lang: str, throw_ex: bool = False) -> str:
    """Traduce un mesaj dintr-o limbă în alta."""
    try:
        source_language = from_lang
        target_languages = [to_lang]
        input_text_elements = [InputTextItem(text=message)]

        response = translator.translate(
            content=input_text_elements, to=target_languages, from_parameter=source_language)
        translation = response[0] if response else None

        if translation:
            translated_text = translation.translations[0]
            return translated_text.text

    except HttpResponseError as exception:
        msg = exception.error.message
        code = exception.error.code
        print(f"Error Code: {exception.error.code}")
        print(f"Message: {msg}")
        if throw_ex:
            raise Exception(code)
        else:
            return msg
