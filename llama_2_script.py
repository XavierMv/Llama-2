import streamlit as st

def gpt_chat():
    st.title("Chat with Llama")
    
    user_txt = st.chat_input("Type your message")
    if user_txt is not None and user_txt != "":

        with st.chat_message("Human"):
            st.write(user_txt)

        with st.chat_message("AI"):
            st.write("Message from AI")

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