from translate import Translator
from dotenv import load_dotenv
import os

load_dotenv()
key = os.getenv("MSKEY")

translator = Translator(
    to_lang="ro", provider="microsoft", from_lang="en", secret_access_key=key, region="francecentral")
translation = translator.translate(
    "Coperta is a type of pasta that originated in Italy and is similar to spaghetti. It has a long, thin shape with ridges on the outside and a flat surface on the inside. Coperta is often served with tomato sauce and meat or cheese.")

print(translation)
