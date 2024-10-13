import re
import streamlit as st
import tinycss2
import openai
from dotenv import load_dotenv
import os

load_dotenv()

# OpenAI API 키 설정 123
openai.api_key = os.getenv("OPENAI_API_KEY")

# CSS 파일과 파싱된 내용을 저장할 변수 (세션 상태에 저장하여 쓰레드 유지)
if 'parsed_css' not in st.session_state:
    st.session_state['parsed_css'] = None
if 'css_content' not in st.session_state:
    st.session_state['css_content'] = None

st.title("HTML + CSS 웹 접근성 수정 도구")

# CSS 파일 업로드
uploaded_file = st.file_uploader("CSS 파일을 업로드하세요", type=["css"])

# CSS 파일이 업로드되었을 때 파싱 및 상태 유지
if uploaded_file is not None:
    css_content = uploaded_file.read().decode('utf-8')
    st.session_state['css_content'] = css_content
    st.session_state['parsed_css'] = tinycss2.parse_stylesheet(css_content)
    st.success("CSS 파일이 성공적으로 업로드 및 파싱되었습니다.")

# 이전에 업로드된 CSS 파일을 유지함
if st.session_state['css_content']:
    st.write("현재 유지 중인 CSS 파일 내용:")
    st.code(st.session_state['css_content'], language='css')

# HTML 코드 입력
html_code = st.text_area("HTML 코드를 입력하세요:")

# HTML 코드에서 사용된 선택자 추출 함수
def extract_selectors(html):
    # 클래스와 아이디 선택자 추출
    classes = re.findall(r'class="([^"]+)"', html)
    ids = re.findall(r'id="([^"]+)"', html)
    
    # 태그 이름 추출
    tags = re.findall(r'<([a-zA-Z0-9]+)', html)
    
    # 중복 제거 후 선택자 리스트로 반환
    selectors = set()
    for class_list in classes:
        selectors.update(['.' + cls.strip() for cls in class_list.split()])  # 클래스는 '.'을 붙여서 사용
    selectors.update(['#' + id_.strip() for id_ in ids])  # 아이디는 '#'을 붙여서 사용
    selectors.update(tags)  # 태그는 그대로 추가

    return selectors

# 선택자가 구조적으로 매칭되는지 확인하는 함수
def is_selector_match(selector_list, selectors):
    for sel in selector_list:
        sel_parts = [part.strip() for part in sel.split('>')]  # '>' 기준으로 선택자를 분리
        # 각 선택자 부분이 HTML에서 추출된 선택자들과 매칭되는지 확인
        match = True
        for part in sel_parts:
            if part not in selectors:  # 각 부분이 추출된 선택자들 중에 있는지 확인
                match = False
                break
        if match:
            return True  # 하나라도 매칭되면 참을 반환
    return False

# CSS에서 선택자와 매칭되는 규칙을 추출하는 함수
def filter_css_by_selectors(parsed_css, selectors):
    filtered_rules = []
    for rule in parsed_css:
        if rule.type == 'qualified-rule':
            # 선택자 부분
            selector_text = ''.join([token.serialize() for token in rule.prelude]).strip()
            selector_list = [s.strip() for s in selector_text.split(',')]
            
            # 각 선택자에 대해 매칭 여부를 구조적으로 확인
            if is_selector_match(selector_list, selectors):
                # 스타일 규칙 부분
                declaration_text = ''.join([token.serialize() for token in rule.content]).strip()
                filtered_rules.append(f"{selector_text} {{ {declaration_text} }}")
    return '\n'.join(filtered_rules)

# 프롬프트 생성 및 API 호출
if st.button("웹 접근성 수정 요청 보내기"):
    if html_code and st.session_state['parsed_css']:
        # HTML 코드에서 선택자 추출
        selectors = extract_selectors(html_code)
        print("추출된 선택자:", selectors)

        # 파싱된 CSS에서 해당 선택자와 관련된 규칙만 필터링
        filtered_css = filter_css_by_selectors(st.session_state['parsed_css'], selectors)
        print("추출된 CSS 규칙:\n", filtered_css)

        if filtered_css:
            st.write("필터링된 CSS 규칙:")
            st.code(filtered_css, language='css')
            
            # HTML과 필터링된 CSS를 조합하여 프롬프트 생성
            prompt = (
                f"다음 HTML과 CSS는 웹 접근성에 문제가 있을 수 있습니다. "
                f"HTML 코드를 우선적으로 수정하여 웹 접근성 문제를 해결해 주세요. "
                f"단, CSS를 수정하지 않고는 문제가 해결되지 않을 경우에만 CSS를 수정해 주세요.\n\n"
                f"HTML:\n{html_code}\n\n"
                f"CSS:\n{filtered_css}\n\n"
                f"CSS를 만일 수정하려면 <style>태그로 감싸서 출력해주세요\n"
                f"순서는 html, css, 설명순이며 수정한 코드를 제외하고는 <, >를 사용하지 말아주세요"
            )
            
            response = openai.ChatCompletion.create(
                model="gpt-4",  # "text-davinci-004" 대신 "gpt-4" 사용
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2048,
                temperature=0.7
            )


            # API 응답 출력
            st.write("웹 접근성 수정 결과:")
            st.write(response.choices[0].message['content'].strip())

        else:
            st.warning("HTML 코드에서 매칭되는 CSS 규칙이 없습니다.")
    else:
        st.error("HTML 코드와 CSS 파일이 필요합니다.")

    st.markdown("### 🌐 수정된 코드 웹에서 확인하기")
    st.components.v1.html(st.session_state.modified_code, height=500, scrolling=True)

