import streamlit as st
import rag_lib as glib

st.set_page_config(page_title="Retrieval-Augmented Generation")
st.title("Retrieval-Augmented Generation")

input_text = st.text_area("Input text", label_visibility="collapsed")
go_button = st.button("Go", type="primary")

if go_button:
    with st.spinner("Working..."):
        response_content, search_results = glib.get_rag_response(question=input_text)
        st.write(response_content)
        with st.expander("See search results"):
            st.table(search_results)
