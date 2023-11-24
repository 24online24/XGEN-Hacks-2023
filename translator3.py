import deepl
from dotenv import load_dotenv
import os

load_dotenv()
key = os.getenv("DEEPLKEY")

translator = deepl.Translator(key)

result = translator.translate_text(
    "Hello, World!", source_lang="EN", target_lang="RO")

print(result.text)
