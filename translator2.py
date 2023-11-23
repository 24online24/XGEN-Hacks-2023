from translate import Translator
# Translate from Romanian to English

translator = Translator(to_lang="ro",)
translation = translator.translate(
    "Coperta is a type of pasta that originated in Italy and is similar to spaghetti. It has a long, thin shape with ridges on the outside and a flat surface on the inside. Coperta is often served with tomato sauce and meat or cheese.")

print(translation)
