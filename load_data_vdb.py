from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders.pdf import PyPDFDirectoryLoader
from langchain.vectorstores import Chroma
from langchain.embeddings import GPT4AllEmbeddings

from translate import Translator
import re

DATA_PATH = "data/"
DB_PATH = "vectorstores/db/"


def create_vector_db():
    loader = PyPDFDirectoryLoader(DATA_PATH)
    documents = loader.load()
    print(f"Processed {len(documents)} pdf files")

    translator_ro_to_en = Translator(to_lang="en", from_lang="ro")

    for doc in documents:
        content = re.sub(r'\s+', ' ', doc.page_content)
        content = content.replace('\n', '').replace('\r', '')
        content = re.sub(r'^[0-9]+\s', '', content, flags=re.MULTILINE)

        if not content.strip():
            documents.remove(doc)
            continue

        # Split the content into chunks of 500 characters
        chunk_size = 500
        content_chunks = [content[i:i+chunk_size]
                          for i in range(0, len(content), chunk_size)]

        # Translate each chunk and combine the translated parts
        translated_parts = []
        for chunk in content_chunks:
            translated_chunk = translator_ro_to_en.translate(chunk)
            translated_parts.append(translated_chunk)

        # Combine the translated parts into a single string
        translated_page_content = ' '.join(translated_parts)

        doc.page_content = translated_page_content

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)
    vectorstore = Chroma.from_documents(
        documents=texts, embedding=GPT4AllEmbeddings(), persist_directory=DB_PATH)
    vectorstore.persist()


if __name__ == "__main__":
    create_vector_db()
