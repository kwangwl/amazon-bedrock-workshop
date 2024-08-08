import streamlit as st
import agent_lib as glib
import uuid


st.set_page_config(page_title="Bedrock Agent Interaction")
st.title("Bedrock Agent Interaction")

# 환경 변수에서 에이전트 ID 및 별칭 ID 가져오기
agent_id = "YL5VOSKPEY"
agent_alias_id = "BI4NJ6MEIE"

# 세션 상태 초기화
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# 텍스트 입력 영역
input_text = st.text_area("질문을 입력하세요", label_visibility="collapsed")
submit_button = st.button("Submit", type="primary")

if submit_button and input_text:
    with st.spinner("응답 생성 중..."):
        # 에이전트 호출
        response = glib.get_agent_response(
            agent_id,
            agent_alias_id,
            st.session_state.session_id,
            input_text
        )

        # 응답 출력
        output_text = response["output_text"]
        st.write("응답:", output_text)

        # 인용 정보 표시
        if response["citations"]:
            with st.expander("인용 정보"):
                for citation in response["citations"]:
                    st.write(citation)

        # 추적 정보 표시
        if response["trace"]:
            with st.expander("추적 정보"):
                for trace_type, traces in response["trace"].items():
                    st.subheader(trace_type)
                    for trace in traces:
                        st.json(trace)