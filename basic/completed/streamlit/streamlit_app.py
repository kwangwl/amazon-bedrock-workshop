import streamlit as st

st.set_page_config(page_title="Streamlit 데모")
st.title("Streamlit 데모")

color_text = st.text_input("가장 좋아하는 색깔을 입력해주세요.")
go_button = st.button("Go", type="primary")

if go_button:
    st.write(f"저도 {color_text} 색깔을 좋아합니다!")
