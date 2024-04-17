import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from src.data_preprocessing import (
    get_pdf_splits, get_text_splits, 
    get_csv_splits, Vector_store)

from langchain_openai import OpenAIEmbeddings

def init_conversation_chain(vector_store):
    """
    Initialize a conversational retrieval chain.
    Args:
        vector_store (langchain.vectorstores.FAISS): Vector store for text chunks.
    Returns:
        langchain.chains.ConversationalRetrievalChain: Initialized conversational chain.
    """
    # Initialize a ChatOpenAI language model
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

    # Create a memory buffer to track conversation history
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=vector_store.as_retriever(), memory=memory
    )
    return conversation_chain

def handle_user_input(user_question, conversation_chain):
    """
    Handle user input and display chatbot responses.
    Args:
        user_question (str): User's input question.
        conversation_chain (langchain.chains.ConversationalRetrievalChain): Conversation chain.
    Returns:
        None
    """
    # Use the conversation chain to generate a response
    response = conversation_chain({"question": user_question})
    # Display the conversation history and responses
    for i, msg in enumerate(response["chat_history"]):
        container_type = "user" if i % 2 == 0 else "assistant"
        container = st.chat_message(container_type)
        container.write(msg.content)

# Function to display the conversation page

def show_conversation_page():
    st.header("Conversation Page")
    # Your conversation display logic goes here
    user_question = st.chat_input(placeholder="Enter your question...")
    if user_question:
        handle_user_input(user_question, st.session_state.conversation)

def show_file_upload_page():
    st.header("Chat with your own documents 💬")
    # upload a PDF file
    file = st.file_uploader("Upload your file: supported file types .txt, .pdf, .csv")
    # extract the file name and extension
    if file is not None:
        file_name = file.name
        extension = file.type.split("/")[-1]

        uploaded_file = None
        if extension == "pdf":
            uploaded_file = get_pdf_splits(file)
        elif extension == "txt":
            uploaded_file = get_text_splits(file)
        elif extension == "csv":
            uploaded_file = get_csv_splits(file)
    
        if uploaded_file is not None:
            # Initialize conversation session state before setting conversation_started
            embeddings_fn = OpenAIEmbeddings()
            index_store = "./index_store.faiss"
            vector_db = Vector_store(uploaded_file, embeddings_fn, index_store=index_store)
            st.session_state.conversation = init_conversation_chain(vector_db)

            # Set session state to indicate conversation has started
            st.session_state.conversation_started = True
            st.experimental_set_query_params(conversation_started=True)
            st.experimental_rerun()  # Rerun the app to display the conversation page
            
        else:
            st.error("File not supported")