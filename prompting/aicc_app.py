import streamlit as st
import aicc_lib as glib

# Task information setup
TASK_INFO = {
    'ko': {
        "상담 요약": ["녹취된 상담의 상세한 요약을 생성합니다.", "summary_ko.txt"],
        "상담 노트": ["필요한 정보만 발췌할 수 있도록 요약 형식을 조정하세요.", "note_ko.txt"],
        "메일 회신": ["고객에게 전달할 회신 메일을 생성하세요.", "reply_ko.txt"],
        "상담 품질": ["녹취에 대한 상세한 규정준수 및 품질을 검토합니다.", "quality_ko.txt"],
    },
    'en': {
        "Consultation Summary": ["Generate a detailed summary of the recorded consultation.", "summary_en.txt"],
        "Consultation Notes": ["Adjust the summary format to extract only necessary information.", "note_en.txt"],
        "Email Reply": ["Generate a reply email to be sent to the customer.", "reply_en.txt"],
        "Consultation Quality": ["Review the transcript for detailed compliance and quality.", "quality_en.txt"],
    }
}

# Streamlit page setup
st.set_page_config(page_title="AICC")
st.title("AICC - Auto Insurance Consultation")

# Language selection
language = st.sidebar.radio("Select Language / 언어 선택", ['en', 'ko'])

# Display the transcript in an expandable area
with open("../resources/aicc_transcription_ko.txt", 'r', encoding='utf-8') as file:
    transcription_text = file.read()
with st.expander("View Transcript / 녹취문 보기"):
    st.write(transcription_text)

# Scenario selection
scenario_name = st.selectbox("Select Scenario / 시나리오 선택", list(TASK_INFO[language].keys()))
description, prompt_name = TASK_INFO[language][scenario_name]
st.write(description)

# Button for generating response and reading prompt to generate response
if st.button(f'Generate {scenario_name} / {scenario_name} 생성'):
    response_placeholder = st.empty()
    with open(f"practice/{prompt_name}", 'r', encoding='utf-8') as file:
        prompt = file.read()
    glib.get_streaming_response(prompt, transcription_text, response_placeholder, language)