import streamlit as st
import aicc_lib as glib
import os


# Task configuration
TASK_INFO = {
    "요약": ["summary", "녹취된 상담의 상세한 요약을 생성합니다.", "요약 생성"],
    "상담노트": ["note", "필요한 정보만 발췌할 수 있도록 요약 형식을 조정하세요.", "상담 노트 생성"],
    "메일 회신": ["reply", "고객에게 전달할 회신 메일을 생성하세요.", "회신 메일 생성"],
    "상담품질": ["quality", "녹취에 대한 상세한 규정준수 및 품질을 검토합니다.", "상담 품질 검토 실행"],
}

st.set_page_config(page_title="AICC")
st.title("AICC - 자동차 보험 상담")

# Title and Audio
st.audio("../resources/aicc_transcription.mp3")

# Expander for transcript
with st.expander("녹취문 보기"):
    with open("../resources/aicc_transcription.txt", 'r', encoding='utf-8') as file:
        transcription_text = file.read()
    st.write(transcription_text)

# Task selection
scenario_name = st.selectbox("시나리오 선택", list(TASK_INFO.keys()))
key_name, description, button_name = TASK_INFO[scenario_name]

# Description and Button
st.write(description)
if st.button(button_name):
    st.write(f"{button_name} 버튼이 클릭되었습니다.")
