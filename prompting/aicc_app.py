import streamlit as st
import aicc_lib as glib

# Task information setup
TASK_INFO = {
    'en': {
        "Consultation Summary": ["Generate a detailed summary of the recorded consultation.", "summary.txt"],
        "Consultation Notes": ["Adjust the summary format to extract only necessary information.", "note.txt"],
        "Email Reply": ["Generate a reply email to be sent to the customer.", "reply.txt"],
        "Consultation Quality": ["Review the transcript for detailed compliance and quality.", "quality.txt"],
    },
    'ko': {
        "상담 요약": ["녹취된 상담의 상세한 요약을 생성합니다.", "summary.txt"],
        "상담 노트": ["필요한 정보만 발췌할 수 있도록 요약 형식을 조정하세요.", "note.txt"],
        "메일 회신": ["고객에게 전달할 회신 메일을 생성하세요.", "reply.txt"],
        "상담 품질": ["녹취에 대한 상세한 규정준수 및 품질을 검토합니다.", "quality.txt"],
    }
}

# Streamlit page setup
st.set_page_config(page_title="AICC", layout="wide")

# Language selection in sidebar
language_options = [('en', 'English'), ('ko', '한국어')]
language = st.sidebar.radio("Language", language_options, format_func=lambda x: x[1])[0]

# Set title based on language
if language == 'en':
    st.title("AICC - Auto Insurance Consultation")
else:
    st.title("AICC - 자동차 보험 상담")

# Display the transcript in an expandable area
transcription_file = f"../resources/aicc_transcription_{language}.txt"
with open(transcription_file, 'r', encoding='utf-8') as file:
    transcription_text = file.read()

if language == 'en':
    with st.expander("View Transcript"):
        st.write(transcription_text)
else:
    with st.expander("녹취문 보기"):
        st.write(transcription_text)

# Scenario selection
scenario_name = st.selectbox(
    "Select Scenario" if language == 'en' else "시나리오 선택",
    list(TASK_INFO[language].keys())
)
description, prompt_name = TASK_INFO[language][scenario_name]
st.write(description)

# Button for generating response and reading prompt to generate response
button_text = f'Generate {scenario_name}' if language == 'en' else f'{scenario_name} 생성'
if st.button(button_text):
    response_placeholder = st.empty()
    with open(f"practice/{prompt_name}", 'r', encoding='utf-8') as file:
        prompt = file.read()
    glib.get_streaming_response(prompt, transcription_text, response_placeholder, language)