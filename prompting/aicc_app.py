import streamlit as st
import aicc_lib as glib

# 작업 정보 설정
TASK_INFO = {
    "요약": ["녹취된 상담의 상세한 요약을 생성합니다.", "summary.txt"],
    "상담노트": ["필요한 정보만 발췌할 수 있도록 요약 형식을 조정하세요.", "note.txt"],
    "메일 회신": ["고객에게 전달할 회신 메일을 생성하세요.", "reply.txt"],
    "상담품질": ["녹취에 대한 상세한 규정준수 및 품질을 검토합니다.", "quality.txt"],
}

# Streamlit 페이지 설정
st.set_page_config(page_title="AICC")
st.title("AICC - 자동차 보험 상담")

# 오디오 파일 표시
st.audio("resources/aicc_transcription.mp3")

# 녹취문을 확장 가능한 영역에 표시
with open("resources/aicc_transcription.txt", 'r', encoding='utf-8') as file:
    transcription_text = file.read()
with st.expander("녹취문 보기"):
    st.write(transcription_text)

# 시나리오 선택
scenario_name = st.selectbox("시나리오 선택", list(TASK_INFO.keys()))
description, prompt_name = TASK_INFO[scenario_name]
st.write(description)

# 응답 생성을 위한 버튼 및 프롬프트 읽어서 응답 생성
if st.button(f'{scenario_name} 생성'):
    response_placeholder = st.empty()
    with open(f"practice/{prompt_name}", 'r', encoding='utf-8') as file:
        prompt = file.read()
    glib.get_streaming_response(prompt, transcription_text, response_placeholder)
