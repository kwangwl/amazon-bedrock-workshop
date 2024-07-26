import streamlit as st
import text_lib as glib

st.set_page_config(page_title="Text to Text")
st.title("Text to Text")

input_text = st.text_area("텍스트 입력", label_visibility="collapsed")
go_button = st.button("Go", type="primary")

if go_button:
    with st.spinner("응답중..."):
        response_content = glib.get_text_response(input_content=input_text)
        st.write(response_content)
