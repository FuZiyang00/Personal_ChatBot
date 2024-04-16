import streamlit as st
from src.data_preprocessing import (
    get_pdf_splits, get_text_splits, 
    get_csv_splits, Vector_store)

from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from src.chatbot_utils import init_conversation_chain, handle_user_input

load_dotenv()

def main(): 
    "main function containing the main logic of the app"

    with st.sidebar:
        st.title('🤗💬 LLM powered Chat bot')
        st.markdown('''
        ## About
        This app is an LLM-powered chatbot built using:
        - [Streamlit](https://streamlit.io/)
        - [LangChain](https://python.langchain.com/)
        - [OpenAI](https://platform.openai.com/docs/models) LLM model
    
        ''')

    st.header("Chat with your own documents 💬")

    # upload a PDF file
    file = st.file_uploader("Upload your file: supported file types .txt, .pdf, .csv")
    # extract the file name and extension
    if file is not None:
        file_name = file.name
        extension = file.type.split("/")[-1]

        uploaded_file = None
        match extension:
            case "pdf":
                uploaded_file = get_pdf_splits(file)

            case "txt":
                uploaded_file = get_text_splits(file)

            case "csv":
                uploaded_file = get_csv_splits(file)
    
        if uploaded_file is not None:
            embeddings_fn = OpenAIEmbeddings()
            index_store = "./index_store.faiss"
            vector_db = Vector_store(uploaded_file, embeddings_fn, index_store=index_store)
            st.success("File uploaded successfully")

            st.session_state.conversation = init_conversation_chain(vector_db)
        else:
            st.error("File not supported")
    
        if st.session_state.conversation:
            user_question = st.chat_input(placeholder="Enter your question...")
            if user_question:
                handle_user_input(user_question, st.session_state.conversation)
        
        #TODO: redirect to a new page after uploading the file: name of the chat is the file name
        #TODO: vector storage: is it possible to check if the file is already uploaded and use the existing vector store?

if __name__ == "__main__":
    main()