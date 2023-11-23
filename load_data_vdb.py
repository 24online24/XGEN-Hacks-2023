from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.document_loaders.pdf import PyPDFDirectoryLoader
from langchain.document_loaders import UnstructuredHTMLLoader, BSHTMLLoader
from langchain.vectorstores import Chroma
from langchain.embeddings import GPT4AllEmbeddings
from langchain.embeddings import OllamaEmbeddings


DATA_PATH = "data_test/"
DB_PATH = "vectorstores/db/"


def create_vector_db():
    loader = PyPDFDirectoryLoader(DATA_PATH)
    documents = loader.load()
    print(f"Processed {len(documents)} pdf files")
    # documents = documents[:10]
    # t5_small_pipeline = pipeline(
    #     task="translation_ro_to_en",
    #     model="t5-small",
    #     max_length=1024,
    #     model_kwargs={
    #         "cache_dir": '/Users/rares/code/hacks2023/XGEN-Hacks-2023/t5_small'}
    # )

    # start_time = time.time()
    # for idx, doc in enumerate(documents):
    #     translated_page_content = t5_small_pipeline(doc.page_content)[0][
    #         'translation_text']
    #     doc.page_content = translated_page_content
    #     if idx % 10 == 0:
    #         print(f"{idx}- {time.time() - start_time} seconds")
    #         start_time = time.time()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)
    vectorstore = Chroma.from_documents(
        documents=texts, embedding=GPT4AllEmbeddings(), persist_directory=DB_PATH)
    vectorstore.persist()


if __name__ == "__main__":
    create_vector_db()
