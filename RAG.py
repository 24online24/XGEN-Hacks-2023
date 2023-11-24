from langchain import hub
from langchain.embeddings import GPT4AllEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import chainlit as cl
from langchain.chains import RetrievalQA, RetrievalQAWithSourcesChain

from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem
from azure.core.exceptions import HttpResponseError

from dotenv import load_dotenv
import os

# Fiecare model (LLM) are un prompt specific optimizat pentru dezvoltarea
# de aplicații de tip retrieval-augmented-generation (chat, întrebare-răspuns).
QA_CHAIN_PROMPT = hub.pull("rlm/rag-prompt-llama")

load_dotenv()
KEY = os.getenv("MSKEY")
ENDPOINT = 'https://api.cognitive.microsofttranslator.com/'
REGION = 'francecentral'

CREDENTIAL = TranslatorCredential(KEY, REGION)
TEXT_TRANSLATOR = TextTranslationClient(
    endpoint=ENDPOINT, credential=CREDENTIAL)


def load_llm():
    """Inițializează modelul dorit. Este recomandată folosirea
    modelelor Mistral sau Llama2."""
    llm = Ollama(
        model="llama2",
        verbose=True,
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    )
    return llm


def retrieval_qa_chain(llm, vectorstore):
    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=vectorstore.as_retriever(),
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
        return_source_documents=False,
    )
    return qa_chain


def qa_bot():
    """Inițializează bot-ul conversațional folosind modelul LLM ales și
    documentele (în cazul nostru cărțile) serializate și stocate în vectorstore."""
    llm = load_llm()
    DB_PATH = "vectorstores/db/"
    vectorstore = Chroma(persist_directory=DB_PATH,
                         embedding_function=GPT4AllEmbeddings())

    qa = retrieval_qa_chain(llm, vectorstore)
    return qa


@cl.on_chat_start
async def start():
    """Funcție apelată la începutul fiecărei conversații noi. Aceasta inițializează
    bot-ul conversațional și îl informază pe utilizator că acesta pornește. Apoi,
    mesajul este actualizat cu întâmpinarea bot-ului. Sesiunea este inițializată,
    folosind actualul "lanț" de mesaje. Acesta va conține conversația."""
    bot = qa_bot()
    msg = cl.Message(content="Firing up the research info bot...")
    await msg.send()
    msg.content = "Hi, welcome to research info bot. What is your query?"
    await msg.update()
    cl.user_session.set("chain", bot)


@cl.on_message
async def main(message):
    """Funcția apelată la fiecare mesaj primit de bot. Acesta va răspunde
    la întrebarea utilizatorului, folosind modelul LLM și documentele stocate
    în vectorstore."""
    bot = cl.user_session.get("chain")
    cb = cl.AsyncLangchainCallbackHandler(
        stream_final_answer=True,
        answer_prefix_tokens=["FINAL", "ANSWER"]
    )
    cb.answer_reached = True
    trasnlated_message = translate_message(message.content, "ro", "en")
    res = await bot.acall(trasnlated_message, callbacks=[cb])
    answer = res["result"]
    answer = answer.replace(".", ".\n")
    translated_answer = translate_message(answer, "en", "ro")

    await cl.Message(content=translated_answer).send()


def translate_message(message: str, from_lang: str, to_lang: str) -> str:
    try:
        source_language = from_lang
        target_languages = [to_lang]
        input_text_elements = [InputTextItem(text=message)]

        response = TEXT_TRANSLATOR.translate(
            content=input_text_elements, to=target_languages, from_parameter=source_language)
        translation = response[0] if response else None

        if translation:
            translated_text = translation.translations[0]
            return translated_text.text

    except HttpResponseError as exception:
        msg = exception.error.message
        print(f"Error Code: {exception.error.code}")
        print(f"Message: {msg}")
        return msg
