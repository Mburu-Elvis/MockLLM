import bs4
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import JSONLoader, PyPDFLoader
from langchain_openai import ChatOpenAI
from pathlib import Path
from pprint import pprint
import gradio as gr
import subprocess
# import getpass
from dotenv import load_dotenv
import os
import glob
import json



load_dotenv()
# os.environ["OPENAI_API_KEY"] = getpass.getpass()
api_key = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=api_key)


vectorStore = ""

def load_pdfs():
    pattern = "*pdf"
    
    directory = os.getcwd()
    
    pdf_files = glob.glob(os.path.join(directory, pattern))

    for file in pdf_files:
        loader = PyPDFLoader(file)
        
        if pdf_files.index(file) == 0:
            pages = loader.load_and_split()
        else:
            pages += loader.load_and_split()
    return pages


def load_json_files():
    pattern = "*json"
    directory = os.getcwd()
    
    json_files = glob.glob(os.path.join(directory, pattern))
    loader = JSONLoader(
                file_path=json_files[0],
                jq_schema='.MedicalHistory[]',
                text_content=False)
    medicalHistroy = loader.load()

    loader = JSONLoader(
        file_path=json_files[1],
        jq_schema='.InsuranceInfo[]',
        text_content=False)
    insurance = loader.load()

    loader = JSONLoader(
        file_path=json_files[2],
        jq_schema='.appointments[]',
        text_content=False)
    appointments = loader.load()

    loader = JSONLoader(
        file_path=json_files[3],
        jq_schema='.Medications[]',
        text_content=False)
    medications = loader.load()
    
    personal_docs = medicalHistroy + insurance + appointments + medications
    
    return personal_docs

def llmPipeline():
    docs = load_pdfs() + load_json_files()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splits = text_splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

    retriever = vectorstore.as_retriever()
    prompt = hub.pull("rlm/rag-prompt")

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)


    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain, vectorstore


def queryChatbot(phoneNumber,userQuery):
    if phoneNumber is not None:
        command = ["./serialize_data.sh", phoneNumber]
        subprocess.call(command)
    
    rag_chain, vectorstore = llmPipeline()
    
    vectorStore = vectorstore
    
    response = rag_chain.invoke(userQuery + "based on the data")
    
    return response

demo = gr.Interface(fn=queryChatbot, inputs=["textbox", "textbox"], outputs="textbox")
    
demo.launch(share=True)

# cleanup
vectorStore.delete_collection()

# if __name__ == "__main__":
#    from flask import Flask, request, jsonify

#    app  = Flask(__name__)
    
#    @app.route('/llm', methods=["POST"])
#    def getResponse():
#        phoneNumber = request.get_json().get('phoneNumber')
#        userQuery = request.get_json().get('userQuery')
#        response = queryChatbot(phoneNumber, userQuery)
       
#        return jsonify({'response': response})

#    app.run(port=5100, debug=True)
#    vectorStore.delete_collection()
