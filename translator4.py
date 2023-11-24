
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem
from azure.core.exceptions import HttpResponseError

from dotenv import load_dotenv
import os

load_dotenv()


key = os.getenv("MSKEY")
endpoint = 'https://api.cognitive.microsofttranslator.com/'
region = 'francecentral'

credential = TranslatorCredential(key, region)
text_translator = TextTranslationClient(endpoint=endpoint, credential=credential)

try:
    source_language = "en"
    target_languages = ["ro"]
    input_text_elements = [ InputTextItem(text = "This is a test") ]

    response = text_translator.translate(content = input_text_elements, to = target_languages, from_parameter = source_language)
    translation = response[0] if response else None

    if translation:
        for translated_text in translation.translations:
            print(f"Text was translated to: '{translated_text.to}' and the result is: '{translated_text.text}'.")

except HttpResponseError as exception:
    print(f"Error Code: {exception.error.code}")
    print(f"Message: {exception.error.message}")