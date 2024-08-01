import streamlit as st
import chatbot_lib as glib

st.set_page_config(page_title="Chatbot")
st.title("Chatbot")

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

chat_container = st.container()
input_text = st.chat_input("여기에서 챗봇과 채팅하세요")

if input_text:
    with st.spinner("응답중..."):
        exceed_limit = glib.converse_with_model(st.session_state.chat_history, input_text)
        if exceed_limit:
            st.warning("최대 메시지 수를 초과하여 메시지 기록이 초기화되었습니다.")

for message in st.session_state.chat_history:
    with chat_container.chat_message(message['role']):
        st.markdown(message['content'][0]['text'])
