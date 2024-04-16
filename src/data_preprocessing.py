from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.document_loaders.csv_loader import CSVLoader
import pandas as pd
from PyPDF2 import PdfReader
import os
     


def get_text_splits(text_file):
    """Function takes in the text data and returns the  
    splits so for further processing can be done."""
    with open(text_file,'r') as txt:
        data = txt.read()

        textSplit = RecursiveCharacterTextSplitter(chunk_size=150,
                                                    chunk_overlap=15,
                                                    length_function=len)
        doc_list = textSplit.split_text(data)
    return doc_list

def get_pdf_splits(pdf_file):
    """Function takes in the pdf data and returns the  
    splits so for further processing can be done."""

    pdf_reader = PdfReader(pdf_file)

    content = ""
    for page in pdf_reader.pages:
        content += page.extract_text()

    text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
            )
    
    chunks = text_splitter.split_text(text=content)
    return chunks

def get_csv_splits(csv_file):
    """Function takes in the csv and returns the  
    splits so for further processing can be done."""
    csvLoader = CSVLoader(csv_file)
    csvdocs = csvLoader.load()
    return csvdocs


def Vector_store(doc_list, embed_fn, index_store):
    """Function takes in existing vector_store, 
    new doc_list and embedding function that is 
    initialized on appropriate model. Local or online. 
    New embedding is merged with the existing index. If no 
    index given a new one is created"""
    #check whether the doc_list is documents, or text
    try:
        faiss_db = FAISS.from_documents(doc_list, embed_fn)  
    except Exception as e:
        faiss_db = FAISS.from_texts(doc_list, embed_fn)
    
    # implementing incremental local vector storage
    if os.path.exists(index_store):
        local_db = FAISS.load_local(index_store,embed_fn, allow_dangerous_deserialization=True)

        #merging the new embedding with the existing index store
        local_db.merge_from(faiss_db)
        print("Merge completed")

        local_db.save_local(index_store)
        print("Updated index saved")

        return local_db

    else:
        faiss_db.save_local(folder_path=index_store)
        print("New store created...")
    
    return faiss_db

        

