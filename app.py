import streamlit as st
from dotenv import load_dotenv
import openai, time, os
import tempfile
import pytesseract
from openai import OpenAI
import backoff
from pathlib import Path
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import HuggingFaceHub
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from pdf2image import convert_from_path
from htmltemp import css, bot_template, user_template
from helppack import inference, tokenize_gpt2, detokenize_gpt2, split_text

MAX_TOKENS = 4000
MAX_NEW_TOKENS = 500

SUMMARY_PREPROMPT = "SUMMARIZE THE FOLLOWING DOCUMENT:\n=====\n"
SUMMARY_POSTPROMPT = "\n=====\nSUMMARY:\n"

SUMMARY_TOKEN_BUDGET = (
    MAX_TOKENS
    - len(tokenize_gpt2(SUMMARY_PREPROMPT))
    - len(tokenize_gpt2(SUMMARY_POSTPROMPT))
    - MAX_NEW_TOKENS
)


@backoff.on_exception(backoff.expo, openai.RateLimitError)
def completions_with_backoff(**kwargs):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return client.chat.completions.create(**kwargs)


def save_uploaded_file(uploaded_file):
    temp_dir = tempfile.mkdtemp()
    path = os.path.join(temp_dir, uploaded_file.name)
    with open(path, "wb") as f:
        f.write(uploaded_file.getvalue())
    return path


def text_from_pdf(pdf_doc, poppler_path):
    pytesseract.pytesseract.tesseract_cmd = (
        r"Tesseract-OCR\tesseract.exe"  # insert the path
    )
    extracted_text = ""
    if pdf_doc:
        images = convert_from_path(pdf_doc, poppler_path=poppler_path)
        for i, image in enumerate(images):
            text = pytesseract.image_to_string(image, lang="eng")
            extracted_text += text
    return extracted_text
    

def get_text_chunks(raw_text):
    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len
    )
    chunks = text_splitter.split_text(raw_text)
    return chunks


def get_vector_store(text_chunks):
    try:
        embeddings = OpenAIEmbeddings()
        vector_store = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
        return vector_store
    except openai.RateLimitError as e:
        st.error(f"Rate limit reached. Please wait and try again in 21 sec")
        time.sleep(21)


def get_convo_chain(vector_store):
    llm = ChatOpenAI()
    memo = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    convo_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(),
        memory=memo,
    )
    return convo_chain


def handle_userinput(user_q):
    try:
        response = st.session_state.convo({"question": user_q})
        st.session_state.chat_history = response["chat_history"]
        for i, msg in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                st.write(
                    user_template.replace("{{MSG}}", msg.content),
                    unsafe_allow_html=True,
                )
            else:
                if (
                    "i don't" in msg.content.lower()
                    or "i'm sorry" in msg.content.lower()
                    or "does not" in msg.content.lower()
                    or "not specified" in msg.content.lower()
                    or "i do not" in msg.content.lower()
                    or "i apologize" in msg.content.lower()
                ):
                    response = completions_with_backoff(
                        model="gpt-3.5-turbo",
                        messages=[
                            {
                                "role": "assistant",
                                "content": """You are a helpful assistant and Start with the sentence, Based on my serach and answer the question.""",
                            },
                            {"role": "user", "content": "{}".format(msg)},
                        ],
                        temperature=1,
                        max_tokens=256,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0,
                    )
                    output = response.choices[0].message.content
                    st.write(
                        bot_template.replace("{{MSG}}", output), unsafe_allow_html=True
                    )
                else:
                    st.write(
                        bot_template.replace("{{MSG}}", msg.content),
                        unsafe_allow_html=True,
                    )
    except openai.RateLimitError as e:
        st.error(f"Rate limit reached. Please wait and try again in 21 seconds.")


def summarize(text, mode="summary"):
    tokenized = tokenize_gpt2(text)
    split = split_text(tokenized, SUMMARY_TOKEN_BUDGET)
    if len(split) > 1:
        summaries = []
        j = 1
        for i, chunk in enumerate(split):
            if j % 3 == 0 and i > 0:  # To avoid Rate limit error
                time.sleep(60)
            chunk_text = detokenize_gpt2(chunk)
            summaries.append(summarize(chunk_text, mode))
            j += 1
        summaries = " ".join(summaries)
    else:
        summaries = text
    prompt = SUMMARY_PREPROMPT + summaries + SUMMARY_POSTPROMPT
    return inference(prompt, MAX_NEW_TOKENS)


def main():
    load_dotenv()
    poppler_path = r"poppler-23.11.0\Library\bin"  # insert the path
    st.set_page_config(page_title="Chat with multiple PDFs", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)
    if "convo" not in st.session_state:
        st.session_state.convo = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    st.header("Chat with multiple PDFs :books:")
    user_q = st.text_input("Ask questions about your documents.")
    if user_q != "":
        handle_userinput(user_q)

    with st.sidebar:
        st.header("YOUR DOCUMENTS")
        pdf_files = st.file_uploader(
            "Upload your PDFs here and 'Process'",
            accept_multiple_files=True,
            type="pdf",
        )
        if st.button("Process"):
            if not pdf_files:
                st.error("Add document")
            else:
                with st.spinner("Processing"):
                    raw_text = ""
                    for uploaded_file in pdf_files:
                        temp_path = save_uploaded_file(uploaded_file)
                        raw_text += text_from_pdf(temp_path, poppler_path)

                    processed_text = str(
                        raw_text.encode("utf-8", errors="replace"), "utf-8"
                    )
                    text_chunks = get_text_chunks(processed_text)
                    with open("file.txt", "w", encoding="utf-8", errors="replace") as f:
                        f.write(str(processed_text))
                    f.close()

                    vector_store = get_vector_store(text_chunks)
                    st.session_state.convo = get_convo_chain(vector_store)

        if st.button("Summarise"):
            with st.spinner("Summarising"):
                file_path = Path("file.txt")
                if not file_path.exists():
                    st.error("Process the document first")
                else:
                    with open("file.txt", "r", encoding="utf-8", errors="replace") as f:
                        text = f.read()
                    f.close()
                    os.remove("file.txt")
                    with open("summary.txt", "w", encoding="utf-8") as f:
                        f.write("SUMMARY :" + "\n")
                    summarize(text)
                    st.success("This is a success message!", icon="✅")


if __name__ == "__main__":
    main()
