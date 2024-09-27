import streamlit as st
import chatbot_lib as glib

st.set_page_config(page_title="Chatbot")
st.title("Chatbot")

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

chat_container = st.container()
input_text = st.chat_input("여기에서 챗봇과 채팅하세요")

if input_text:
    st.session_state.chat_history.append({"role": "user", "content": [{"text": input_text}]})

    with st.spinner("응답중..."):
        response = glib.get_response(st.session_state.chat_history)
        output = glib.handle_response(response)

        st.session_state.chat_history.append({"role": "assistant", "content": [{"text": output}]})

for message in st.session_state.chat_history:
    with chat_container.chat_message(message['role']):
        st.markdown(message['content'][0]['text'])
