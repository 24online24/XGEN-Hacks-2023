from datasets import load_dataset
from transformers import pipeline

# Pipeline for translation from English to Romanian
t5_small_pipeline = pipeline(
    task="text2text-generation",
    model="t5-small",
    max_length=50,
    model_kwargs={
        "cache_dir": '/Users/rares/code/hacks2023/XGEN-Hacks-2023/t5_small'}
)
x = t5_small_pipeline("translate Romanian to English : Salut, ce mai faci?")[
    0]['generated_text']
print(x)
