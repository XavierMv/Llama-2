import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage # This functions will help us create a chat history

def gpt_chat():
    st.title("Chat with Llama")

    def get_answer(user_input):
        return "I don't know"
    
    chat_history = [AIMessage("Hello! How can I help you?"),]    
    user_txt = st.chat_input("Type your message")
    if user_txt is not None and user_txt != "":
        response = get_answer(user_txt)
        chat_history.append(HumanMessage(content = user_txt))
        chat_history.append(AIMessage(content = response))
        
        with st.chat_message("Human"):
            st.write(user_txt)
        with st.chat_message("AI"):
            st.write(response)















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