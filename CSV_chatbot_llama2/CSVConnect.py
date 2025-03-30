import streamlit as st
from streamlit_chat import message
import tempfile
import textwrap
from huggingface_hub import hf_hub_download
from langchain.document_loaders import CSVLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import CTransformers
from langchain.chains import ConversationalRetrievalChain

st.set_page_config(page_title="Chat with CSV using LLaMA2", layout="wide")

# ✅ Constants
DB_FAISS_PATH = 'vectorstore/db_faiss'
BACKGROUND_IMAGE_PATH = 'background.jpg'
MODEL_REPO = "TheBloke/Llama-2-7B-Chat-GGML"
MODEL_FILE = "llama-2-7b-chat.ggmlv3.q8_0.bin"

# ✅ Load LLaMA-2 Model
def load_llm():
    """
    Downloads and loads the LLaMA-2 GGML model correctly.
    """
    model_path = hf_hub_download(repo_id=MODEL_REPO, filename=MODEL_FILE, local_dir="./models")

    llm = CTransformers(
        model=model_path,  # Use the downloaded model path
        model_type="llama",  # Explicitly define model type
        max_new_tokens=512,
        temperature=0.1,
        gpu_layers=50  # Set GPU layers for acceleration if available
    )

    return llm

# ✅ Streamlit UI Setup
st.title("☔ Chat with CSV using LLaMA2 ☔")
st.markdown("Built by ♻️ CSVQConnect ♻️", unsafe_allow_html=True)

# ✅ File Upload
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    # ✅ Process uploaded CSV file
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

    # ✅ Load Data & Create Vector Store
    loader = CSVLoader(file_path=tmp_file_path, encoding="utf-8", csv_args={'delimiter': ','})
    data = loader.load()

    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    db = FAISS.from_documents(data, embeddings)
    db.save_local(DB_FAISS_PATH)

    # ✅ Load LLM and Retrieval Chain
    llm = load_llm()
    chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=db.as_retriever())

    # ✅ Conversational Chat Function (Fixes Token Limit Issues)
    def conversational_chat(query):
        """
        Processes long queries using token chunking and sliding window approach.
        """
        max_chunk_size = 400  # Keep it well below model limit (512)
        query_chunks = textwrap.wrap(query, max_chunk_size, break_long_words=False)

        chat_history = st.session_state.get('history', [])

        # ✅ Ensure history is within token limits (keep last 3 messages)
        chat_history = chat_history[-3:]

        # ✅ Generate concise chat history summary to reduce token load
        if len(chat_history) > 0:
            chat_summary = " ".join([f"User: {q} | Bot: {a}" for q, a in chat_history])
            if len(chat_summary.split()) > 200:  # Prevent history bloat
                chat_summary = chat_summary[-200:]  # Trim older parts
        else:
            chat_summary = ""

        results = []

        for chunk in query_chunks:
            try:
                result = chain.invoke({"question": chunk, "chat_history": chat_summary})
                chat_history.append((chunk, result["answer"]))
                results.append(result["answer"])
            except Exception as e:
                st.error(f"❌ Model Error: {e}")

        st.session_state['history'] = chat_history  # Update session history
        return " ".join(results)


    # ✅ Initialize Chat History
    if 'history' not in st.session_state:
        st.session_state['history'] = []

    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hello! What is your query about " + uploaded_file.name + " 🤗"]

    if 'past' not in st.session_state:
        st.session_state['past'] = ["Hey! 👋"]

    # ✅ UI Layout for Chat
    response_container = st.container()
    container = st.container()

    with container:
        with st.form(key='chat_form', clear_on_submit=True):
            user_input = st.text_input("Query:", placeholder="Ask a question about your CSV data...", key='input')
            submit_button = st.form_submit_button(label='Send')

        if submit_button and user_input:
            output = conversational_chat(user_input)

            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output)

    if st.session_state['generated']:
        with response_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="big-smile")
                message(st.session_state["generated"][i], key=str(i), avatar_style="thumbs")
