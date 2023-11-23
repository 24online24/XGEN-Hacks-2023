from langchain import hub
from langchain.embeddings import GPT4AllEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import chainlit as cl
from langchain.chains import RetrievalQA, RetrievalQAWithSourcesChain
# Fiecare model (LLM) are un prompt specific optimizat pentru dezvoltarea
# de aplicații de tip retrieval-augmented-generation (chat, întrebare-răspuns).
QA_CHAIN_PROMPT = hub.pull("rlm/rag-prompt-mistral")


def load_llm():
    """Inițializează modelul dorit. Este recomandată folosirea
    modelelor Mistral sau Llama2."""
    llm = Ollama(
        model="mistral",
        verbose=True,
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    )
    return llm


def retrieval_qa_chain(llm, vectorstore):
    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=vectorstore.as_retriever(),
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
        return_source_documents=True,
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
    chain = qa_bot()
    msg = cl.Message(content="Firing up the research info bot...")
    await msg.send()
    msg.content = "Hi, welcome to research info bot. What is your query?"
    await msg.update()
    cl.user_session.set("chain", chain)


@cl.on_message
async def main(message):
    """Funcția apelată la fiecare mesaj primit de bot. Acesta va răspunde
    la întrebarea utilizatorului, folosind modelul LLM și documentele stocate
    în vectorstore."""
    chain = cl.user_session.get("chain")
    cb = cl.AsyncLangchainCallbackHandler(
        stream_final_answer=True,
        answer_prefix_tokens=["FINAL", "ANSWER"]
    )
    cb.answer_reached = True
    # res=await chain.acall(message, callbacks=[cb])
    res = await chain.acall(message.content, callbacks=[cb])
    print(f"response: {res}")
    answer = res["result"]
    answer = answer.replace(".", ".\n")
    sources = res["source_documents"]

    if sources:
        answer += f"\nSources: "+str(str(sources))
    else:
        answer += f"\nNo Sources found"

    await cl.Message(content=answer).send()
