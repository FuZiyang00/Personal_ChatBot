import streamlit as st
from src.chatbot_utils import show_conversation_page, show_file_upload_page
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

    if 'conversation_started' in st.session_state:
        # If conversation has started, display conversation page
        show_conversation_page()
    else:
        # Display file upload page
        show_file_upload_page()

        
        
if __name__ == "__main__":
    main()