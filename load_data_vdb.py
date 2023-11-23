from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders.pdf import PyPDFDirectoryLoader
from langchain.vectorstores import Chroma
from langchain.embeddings import GPT4AllEmbeddings

from translate import Translator
import time

DATA_PATH = "data/"
DB_PATH = "vectorstores/db/"


def create_vector_db():
    loader = PyPDFDirectoryLoader(DATA_PATH)
    documents = loader.load()
    print(f"Processed {len(documents)} pdf files")
    translator_ro_to_en = Translator(to_lang="en", from_lang="ro")

    start_time = time.time()
    for idx, doc in enumerate(documents):
        translated_page_content = translator_ro_to_en.translate(
            doc.page_content)
        doc.page_content = translated_page_content
        if idx % 10 == 0:
            print(f"{idx}- {time.time() - start_time} seconds")
            start_time = time.time()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)
    vectorstore = Chroma.from_documents(
        documents=texts, embedding=GPT4AllEmbeddings(), persist_directory=DB_PATH)
    vectorstore.persist()


if __name__ == "__main__":
    create_vector_db()
