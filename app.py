import streamlit as st
from PyPDF2 import PdfReader

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

    st.header("Chat with your own pdf document 💬")

    # upload a PDF file
    pdf = st.file_uploader("Upload your PDF", type='pdf')
 
    # st.write(pdf)
    if pdf is not None:
        pdf_reader = PdfReader(pdf)

        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        st.write(text[:-1])

if __name__ == "__main__":
    main()