import streamlit as st

def gpt_chat():
    st.title("Chat with Llama")


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