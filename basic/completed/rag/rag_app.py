import streamlit as st  # Streamlit 라이브러리 임포트
import rag_lib as glib  # 로컬 라이브러리 스크립트 임포트

# HTML 페이지 제목과 페이지 제목을 설정합니다.
st.set_page_config(page_title="Retrieval-Augmented Generation")
st.title("Retrieval-Augmented Generation")

# 세션 상태에 벡터 인덱스가 없는지 확인하고, 없으면 벡터 인덱스를 생성하고 세션 상태에 저장합니다.
if 'vector_index' not in st.session_state:
    with st.spinner("Indexing document..."):
        embeddings = glib.create_embeddings()
        pdf_path = "Amazon-com-Inc-2023-Shareholder-Letter.pdf"
        loader = glib.load_pdf(pdf_path)
        text_splitter = glib.create_text_splitter()
        st.session_state.vector_index = glib.create_vector_index(embeddings, text_splitter, loader)

# 사용자가 질문을 입력할 수 있는 텍스트 상자와 "Go" 버튼을 제공합니다.
input_text = st.text_area("Input text", label_visibility="collapsed")
go_button = st.button("Go", type="primary")

# 버튼 클릭 시 동작
if go_button:
    with st.spinner("Working..."):
        llm = glib.create_llm()
        response_contents = glib.generate_rag_response(
            index=st.session_state.vector_index,
            question=input_text,
            llm=llm,
        )

        st.write(response_contents)  # 응답 콘텐츠 표시
