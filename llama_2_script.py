import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
import torch
from transformers import LlamaForCausalLM, LlamaTokenizer, AutoModelForCausalLM, AutoTokenizer
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.retrievers import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain


model_path = "./llama/llama-2-7b-chat"
tokenizer_path = "./llama"
model = AutoModelForCausalLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)

def gpt_chat():
    st.title("Chat with Llama")

    # We load the URL we wish to analyze and split the text from the Url into chunks
    def get_vectorstore_from_url(url):
        loader = WebBaseLoader(url) # Load
        document = loader.load()

        text_splitter = RecursiveCharacterTextSplitter() # Split into Chunks
        document_chunks = text_splitter.split_documents(document)

        vector_store = Chroma.from_documents(document_chunks, OpenAIEmbeddings()) # Chroma is used for the embeddings of the document

        return vector_store

    # This function uses the LLM model to search data on the url provided
    def get_context_retriever_chain(vector_store):
        model = AutoModelForCausalLM.from_pretrained(model_path)
        tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)

        retriever = vector_store.as_retriever()
        prompt = ChatPromptTemplate.from_messages([
            MessagesPlaceholder(variable_name = "chat_history"),
            ("user", "{input}"),
            ("user", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
        ])

        retriever_chain = create_history_aware_retriever(model, retriever, prompt)


    # reads the whole conversation and creates an answer based on all the chat history
    def get_conversational_rag_chain(retriever_chain):
        model = AutoModelForCausalLM.from_pretrained(model_path)
        tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)

        prompt = ChatPromptTemplate.from_messages([
            ("system", "Answer the user's questions based on the below context:\n\n{context}"), 
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            ])
    
        stuff_documents_chain = create_stuff_documents_chain(model, prompt)
        
        return create_retrieval_chain(retriever_chain, stuff_documents_chain)


    def get_answer(user_input):
        return "I don't know"
            
    
    

    with st.sidebar:
        st.header("Settings Menu")
        website_url = st.text_input("Website URL")

        if website_url is None or website_url == "":
            st.info("Please enter a website URL")

        else:
            # session state
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = [
                    AIMessage(content = "Hello! How can I help you?"),
                ]
            if "vector_store" not in st.session_state:
                st.session_state.vector_store = get_vectorstore_from_url(website_url) 

    user_txt = st.chat_input("Type your message")
    if user_txt is not None and user_txt != "":
        answer = get_answer(user_txt)
        st.session_state.chat_history.append(HumanMessage(content = user_txt))
        st.session_state.chat_history.append(AIMessage(content = answer))
        
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.write(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.write(message.content)















def gpt_chat_spanish():
    st.title("We will be using Llama... para hablar en español!")

def llama2():
    st.title("Llama")

def main():
    st.sidebar.title("Navigation")
    pages = {
        "GPT Chat": gpt_chat,
        "GPT en Español": gpt_chat_spanish,
        "Llama": llama2
    }

    selected_page = st.sidebar.selectbox("Select a page", list(pages.keys()))

    pages[selected_page]()

if __name__ == "__main__":
    main()