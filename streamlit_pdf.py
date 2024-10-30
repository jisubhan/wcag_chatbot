import streamlit as st
from streamlit_ace import st_ace  # 코드 편집기를 위한 모듈
import tinycss2 #css 파싱
import chatbot_gpt
import os
import difflib  # 코드 비교를 위한 모듈

# 'guide.pdf' 파일을 data 디렉토리에서 로드
pdf_file_path = "data/wcag.pdf"

# 'wcag.txt' 파일을 data 디렉토리에서 로드
txt_file_path = "data/long.txt"

# 벡터 스토어 디렉토리 경로 생성
vector_store_dir = os.path.join(os.getcwd(), os.path.splitext(os.path.basename(pdf_file_path))[0])

# 페이지 설정
st.set_page_config(layout="wide", page_title="🧑🏻‍💻 웹 콘텐츠 수정 자동화 챗봇")

# CSS 파일과 파싱된 내용을 저장할 변수 (세션 상태에 저장하여 쓰레드 유지)
if 'parsed_css' not in st.session_state:
    st.session_state['parsed_css'] = None
if 'css_content' not in st.session_state:
    st.session_state['css_content'] = None

# 페이지 제목
st.title("🧑🏻‍💻 웹접근성 수정 자동화 챗봇")

# 먼저 기존 벡터 스토어가 있는지 확인하고, 없으면 새로 임베딩 처리
vector_store = chatbot_gpt.load_vector_store(vector_store_dir)
if vector_store:
    print("yes")
else:
    vector_store = chatbot_gpt.embed_pdf(pdf_file_path, vector_store_dir)


# 접근성 지침 요약 로드
def load_guidelines_summary(): 
    with open("data/wcag.txt", "r", encoding="utf-8") as file:
        summary = file.read()
    return summary

if "guidelines_summary" not in st.session_state:
    with st.spinner("웹 접근성 지침 요약을 로드하고 있습니다..."):
        guidelines_summary = load_guidelines_summary()
        st.session_state.guidelines_summary = guidelines_summary

option = st.selectbox(
    '예시 질문을 입력하세요',
    ('웹접근성지침에 맞게 코드를 수정해줘', '이미지에 대체 텍스트를 추가해줘', '폼 요소에 레이블을 추가해줘', '직접입력')
)

# 코드 수정 요청 입력
if option == '직접입력':
    code_prompt = st.text_input("코드 수정이나 생성에 대한 요청을 입력하세요.", placeholder="예: 웹접근성지침에 맞게 코드를 수정해줘")
else:
    code_prompt = option

# 코드 편집 및 자동 수정 섹션
st.markdown("💻 코드 편집 및 자동 수정")

# 코드 편집기 설정
if "user_code" not in st.session_state:
    st.session_state.user_code = ""

user_code = st_ace(
    value=st.session_state.user_code,
    language='html',
    #theme='monokai',
    theme='dawn',
    keybinding='vscode',
    font_size=14,
    tab_size=4,
    min_lines=10,
    key="ace_editor",
    auto_update=True,
)

# CSS 파일 업로드
uploaded_file = st.file_uploader("CSS 파일을 업로드하세요", type=["css"])

# CSS 파일이 업로드되었을 때 파싱 및 상태 유지
if uploaded_file is not None:
    css_content = uploaded_file.read().decode('utf-8')
    st.session_state['css_content'] = css_content
    st.session_state['parsed_css'] = tinycss2.parse_stylesheet(css_content)
    st.success("CSS 파일이 성공적으로 업로드 및 파싱되었습니다.")


# 코드 저장
filtered_css = ""
st.session_state.user_code = user_code
st.session_state.filtered_css = filtered_css

# 코드 생성/수정 버튼
if st.button("✨ 코드 생성/수정"):
    if code_prompt and user_code:
        if st.session_state['parsed_css']:
            # HTML 코드에서 선택자 추출
            selectors = chatbot_gpt.extract_selectors(user_code)

            # 파싱된 CSS에서 해당 선택자와 관련된 규칙만 필터링
            filtered_css = chatbot_gpt.filter_css_by_selectors(st.session_state['parsed_css'], selectors)

            if filtered_css:
                st.write("필터링된 CSS 규칙:")
                st.code(filtered_css, language='css')
                st.session_state.filtered_css = "<style>"+"\n"+filtered_css+"\n"+"</style>"

        with st.spinner("AI가 코드를 생성/수정하고 있습니다..."):
            try:
                #쿼리 변수 추가
                query = user_code+"\n"+filtered_css
                if query:
                    # 가장 관련성이 높은 텍스트 검색
                    docs = vector_store.similarity_search(query)
                    relevant_text = "\n".join([doc.page_content for doc in docs])

                # AI를 통한 코드 생성 (chatbot_gpt.py에서 함수 호출)
                modified_code = chatbot_gpt.generate_code(code_prompt, user_code, filtered_css, st.session_state.guidelines_summary)
                st.success("코드 생성/수정이 완료되었습니다.")
                extracted_html, extracted_css = chatbot_gpt.extract_html_css_from_response(modified_code)
                # 생성된 코드를 세션 상태에 저장
                st.session_state.extracted_html = extracted_html
                if extracted_css:
                    st.session_state.extracted_css = extracted_css
                else:
                    extracted_css = ""
                    st.session_state.extracted_css = "<style>"+"\n"+filtered_css+"\n"+"</style>"
                # 수정 사항 설명 요청 (chatbot_gpt.py에서 함수 호출)
                explanation = chatbot_gpt.generate_explanation(user_code, filtered_css, modified_code, relevant_text)
                
                st.session_state.explanation = explanation
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
    else:
        st.warning("코드와 수정 요청을 모두 입력해주세요.")

# 수정된 코드 미리보기
# 수정된 코드와 차이점 표시
if "extracted_html" in st.session_state:
    st.markdown("### 📝 수정된 코드")   
    st.code(st.session_state.extracted_html, language='html')

    st.markdown("### 🖍 수정된 코드와 차이점")
    
    original_code_lines = st.session_state.user_code.splitlines() + st.session_state.filtered_css.splitlines()
    modified_code_lines = st.session_state.extracted_html.splitlines() + st.session_state.extracted_css.splitlines()

    # HTML Diff 생성
    diff = difflib.HtmlDiff(wrapcolumn=60).make_table(
        original_code_lines,
        modified_code_lines,
        fromdesc='원본 코드',
        todesc='수정된 코드',
        context=True,
        numlines=5
    )
    
    # 스타일 수정
    # 스타일 수정 (다크 모드 대응)
    diff_style = """
    <style>
    table.diff {width: 100%; font-family: Courier; border-collapse: collapse;}
    .diff_header {background-color: #e0e0e0; color: #000;}
    .diff_next {background-color: #c0c0c0; color: #000;}
    .diff_add {background-color: #a6f3a6; color: #000;}
    .diff_chg {background-color: #ffff77; color: #000;}
    .diff_sub {background-color: #f7c0c0; color: #000;}
    td, th {padding: 5px;}
    /* 다크 모드 스타일 */
    @media (prefers-color-scheme: dark) {
        table.diff {background-color: #2e2e2e; color: #fff;}
        .diff_header {background-color: #444; color: #fff;}
        .diff_next {background-color: #666; color: #fff;}
        .diff_add {background-color: #335533; color: #fff;}
        .diff_chg {background-color: #888833; color: #fff;}
        .diff_sub {background-color: #663333; color: #fff;}
    }
    </style>
    """
    
    # diff_html에 스타일 추가
    diff_html = diff_style + diff
    
    st.markdown("아래 표는 원본 코드와 수정된 코드의 차이점을 보여줍니다. 추가된 부분은 초록색으로, 삭제된 부분은 빨간색으로 표시됩니다.")
    
    # Diff 결과 표시
    st.components.v1.html(diff_html, height=600, scrolling=True)

    # 수정 사항 설명 표시
    if "explanation" in st.session_state and st.session_state.explanation:
        st.markdown("### 💬 수정 사항 설명")
        st.info(st.session_state.explanation)

        st.markdown("### 🌐 수정전 코드 웹에서 확인하기")
        st.components.v1.html(f"<style>{filtered_css}</style>\n{user_code}", height=500, scrolling=True)

        st.markdown("### 🌐 수정된 코드 웹에서 확인하기")
        # HTML과 CSS를 렌더링
        if extracted_html:
            # CSS가 없는 경우 필터링된 CSS 사용
            if not extracted_css:
                st.components.v1.html(f"<style>{filtered_css}</style>\n{extracted_html}", height=500, scrolling=True)
            else:
                # HTML과 CSS가 모두 있을 경우 함께 렌더링
                st.components.v1.html(f"{extracted_css}\n{extracted_html}", height=500, scrolling=True)

