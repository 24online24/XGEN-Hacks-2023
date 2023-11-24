from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders.pdf import PyPDFDirectoryLoader
from langchain.vectorstores import Chroma
from langchain.embeddings import GPT4AllEmbeddings

from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem
from azure.core.exceptions import HttpResponseError

from dotenv import load_dotenv
import os
import re
import time

DATA_PATH = "data/"
DB_PATH = "vectorstores/db/"


def create_vector_db():
    load_dotenv()
    key = os.getenv("MSKEY")
    endpoint = 'https://api.cognitive.microsofttranslator.com/'
    region = 'francecentral'

    credential = TranslatorCredential(key, region)
    text_translator = TextTranslationClient(
        endpoint=endpoint, credential=credential)

    loader = PyPDFDirectoryLoader(DATA_PATH)
    documents = loader.load()
    print(f"Processed {len(documents)} pdf files")
    exponential_backoff = 1
    for idx, doc in enumerate(documents):
        content = re.sub(r'\s+', ' ', doc.page_content)
        content = content.replace('\n', '').replace('\r', '')
        content = re.sub(r'^[0-9]+\s', '', content, flags=re.MULTILINE)

        if not content.strip():
            documents.remove(doc)
            continue

        try:
            source_language = "ro"
            target_languages = ["en"]
            input_text_elements = [InputTextItem(text=content)]

            response = text_translator.translate(
                content=input_text_elements, to=target_languages, from_parameter=source_language)
            translation = response[0] if response else None

            if translation:
                translated_text = translation.translations[0]
                translated_page_content = translated_text.text

            if exponential_backoff > 1:
                exponential_backoff /= 2
                print(f"Exponential backoff: {exponential_backoff}")

        except HttpResponseError as exception:
            error_code = exception.error.code
            print(f"Error Code: {error_code}")
            print(f"Message: {exception.error.message}")
            if error_code == 429001 and exponential_backoff < 16:
                exponential_backoff *= 2
                print(f"Exponential backoff: {exponential_backoff}")
            translated_page_content = ""

        with open('translated.txt', 'a') as f:
            try:
                f.write(translated_page_content)
            except UnicodeEncodeError:
                pass
        doc.page_content = translated_page_content
        if idx % 10 == 0:
            print(f"Translated {idx} documents")
        time.sleep(exponential_backoff)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)
    vectorstore = Chroma.from_documents(
        documents=texts, embedding=GPT4AllEmbeddings(), persist_directory=DB_PATH)
    vectorstore.persist()


if __name__ == "__main__":
    create_vector_db()
