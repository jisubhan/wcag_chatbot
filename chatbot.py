import os
import streamlit as st
from streamlit_ace import st_ace  # 코드 편집기를 위한 모듈
import openai  # AI 코드 생성을 위한 모듈
from dotenv import load_dotenv
from generate_code import generate_code  # generate_code 함수 임포트
from generation_explanation import generate_explanation  # generate_explanation 함수 임포트
load_dotenv()

# OpenAI API 키 설정 123
openai.api_key = os.getenv("OPENAI_API_KEY")

# 페이지 설정
st.set_page_config(page_title="🧑🏻‍💻 웹 콘텐츠 수정 자동화 챗봇")

# 페이지 제목
st.title("🧑🏻‍💻 웹 콘텐츠 수정 자동화 챗봇")

# 접근성 지침 요약 로드
def load_guidelines_summary(): 
    with open("data/wcag.txt", "r", encoding="utf-8") as file:
        summary = file.read()
    return summary

if "guidelines_summary" not in st.session_state:
    with st.spinner("웹 접근성 지침 요약을 로드하고 있습니다..."):
        guidelines_summary = load_guidelines_summary()
        st.session_state.guidelines_summary = guidelines_summary

st.write("🇰🇷 한국형 웹 콘텐츠 접근성 지침을 바탕으로 코드를 수정해보세요 🤖")

# 예시 질문 아코디언
with st.expander("예시 질문 보기"):
    st.markdown("""
    - 웹 접근성 문제를 해결해줘
    - 이미지에 대체 텍스트를 추가해줘
    - 폼 요소에 레이블을 추가해줘
    """)

# 코드 편집 및 자동 수정 섹션
st.subheader("💻 코드 편집 및 자동 수정")

# 코드 편집기 설정
if "user_code" not in st.session_state:
    st.session_state.user_code = ""

user_code = st_ace(
    value=st.session_state.user_code,
    language='html',
    theme='monokai',
    keybinding='vscode',
    font_size=14,
    tab_size=4,
    min_lines=10,
    key="ace_editor",
    auto_update=True,
)

# 코드 저장
st.session_state.user_code = user_code

# 코드 수정 요청 입력
st.markdown("### 💡 코드 수정 요청")
code_prompt = st.text_input("코드 수정이나 생성에 대한 요청을 입력하세요.", placeholder="예: 웹 접근성 문제를 해결해줘")

# 코드 생성/수정 버튼
if st.button("✨ 코드 생성/수정"):
    if code_prompt and user_code:
        with st.spinner("AI가 코드를 생성/수정하고 있습니다..."):
            try:
                # AI를 통한 코드 생성
                modified_code = generate_code(code_prompt, user_code, st.session_state.guidelines_summary)
                st.success("코드 생성/수정이 완료되었습니다.")
                # 생성된 코드를 세션 상태에 저장
                st.session_state.modified_code = modified_code
                # 수정 사항 설명 요청
                explanation = generate_explanation(user_code, modified_code)
                st.session_state.explanation = explanation
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
    else:
        st.warning("코드와 수정 요청을 모두 입력해주세요.")

# 수정된 코드 미리보기
if "modified_code" in st.session_state:
    st.markdown("### 📝 수정된 코드")   
    st.code(st.session_state.modified_code, language='html')

    st.markdown("### 🌐 수정된 코드 웹에서 확인하기")
    st.components.v1.html(st.session_state.modified_code, height=500, scrolling=True)

    # 수정 사항 설명 표시
    if "explanation" in st.session_state and st.session_state.explanation:
        st.markdown("### 💬 수정 사항 설명")
        st.info(st.session_state.explanation)
