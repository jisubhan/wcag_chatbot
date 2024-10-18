import openai
import streamlit as st
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader
import os
import re


# .env 파일에서 OpenAI API 키 로드
load_dotenv()

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

# 'guide.pdf' 파일을 data 디렉토리에서 로드
pdf_file_path = "data/wcag.pdf"

# 'wcag.txt' 파일을 data 디렉토리에서 로드
txt_file_path = "data/long.txt"

# 벡터 스토어 디렉토리 경로 생성
#vector_store_dir = os.path.join(os.getcwd(), os.path.splitext(os.path.basename(pdf_file_path))[0])

# 벡터 스토어가 이미 존재하는지 확인하고, 존재하면 로드
def load_vector_store(directory):
    faiss_index_path = os.path.join(directory,"index.faiss")
    print("faiss_index_path="+faiss_index_path)
    if os.path.exists(faiss_index_path):
        # FAISS 벡터 스토어 로드
        vector_store = FAISS.load_local(directory, OpenAIEmbeddings(), allow_dangerous_deserialization=True)
        return vector_store
    return None

# 텍스트 파일 읽기 함수 정의
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

# 텍스트 분할 함수 (너무 긴 텍스트는 나눕니다)
def split_text(text, chunk_size=1000, chunk_overlap=200):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    return text_splitter.split_text(text)

# PDF 임베딩 및 벡터 스토어 생성
def embed_pdf(pdf_file_path, directory):
    # PDF 파일 읽기
    with open(pdf_file_path, "rb") as pdf_file:
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()

    
    # 텍스트 분할
    chunks = split_text(text)

    # OpenAI 임베딩 모델 사용 (기본적으로 text-embedding-ada-002 사용)
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    
    # FAISS 벡터 스토어 생성 및 텍스트 임베딩
    vector_store = FAISS.from_texts(chunks, embedding=embeddings)
    
    # 디렉토리가 없으면 생성
    if not os.path.exists(directory):
        os.makedirs(directory)

    # 벡터 스토어를 로컬에 저장
    vector_store.save_local(directory)

    return vector_store

# 텍스트 임베딩 및 벡터 스토어 생성
def embed_text(text_file_path, directory):
    # 텍스트 파일 읽기
    text = read_text_file(text_file_path)

    # 텍스트 분할
    chunks = split_text(text)

    # OpenAI 임베딩 모델 사용 (기본적으로 text-embedding-ada-002 사용)
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

    # FAISS 벡터 스토어 생성 및 텍스트 임베딩
    vector_store = FAISS.from_texts(chunks, embedding=embeddings)

    # 디렉토리가 없으면 생성
    if not os.path.exists(directory):
        os.makedirs(directory)

    # 벡터 스토어를 로컬에 저장
    vector_store.save_local(directory)

    return vector_store


# OpenAI API를 사용하여 코드 생성 함수 정의
def generate_code(prompt, code, filtered_css, guidelines):
    full_prompt = f"""
당신은 웹 접근성 전문가입니다. 아래의 웹 콘텐츠 접근성 지침 요약을 참고하여, 
사용자가 제공한 HTML코드와 css코드를 바탕으로 '{prompt}' 요청에 따라 수정하세요. 단 우선적으로 
html코드를 수정해야하며 어쩔 수 없는 경우에만 css코드를 수정하세요\n
웹 콘텐츠 접근성 지침 요약:\n
{guidelines}\n
사용자 제공 HTML 코드:\n
{code}\n
사용자 제공 HTML 코드:\n
{filtered_css}\n
html코드는 <html>태그로 감싸서 출력해주세요\n
CSS를 만일 수정하려면 <style>태그로 감싸서 출력해주세요\n
 설명, 다른 문자없이 오직 순서는 html, css 순으로 
 가독성이 좋게 코드의 줄바꿈 및 들여쓰기 해서 수정된 코드만 제공해주세요. 
"""
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": full_prompt}],
        max_tokens=2048,
        temperature=0,
        n=1,
        stop=None,
    )
    generated_code = response.choices[0].message.content.strip()
    return generated_code
    


def generate_explanation(original_code, filtered_css, modified_code, relevant_text):
    explanation_prompt = f"""
    다음은 사용자가 제공한 원본 코드와 CSS입니다.\n원본 코드:{original_code}\n CSS"{filtered_css}\n
    그리고 다음은 수정된 코드입니다.\n수정된 코드:{modified_code}\n
    "웹접근성지침" 항목으로 {relevant_text}를 이해하기 좋게 정리해서 출력하고 이후 수정 사항을 간략히 설명해주세요.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": explanation_prompt}],
        max_tokens=2048,
        temperature=0,
        n=1,
        stop=None
    )
    explanation = response.choices[0].message.content.strip()
    return explanation

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

# AI 응답에서 HTML과 CSS 코드를 추출하는 함수
def extract_html_css_from_response(response_content):
    # HTML 부분 추출
    html_match = re.search(r"<html\b[^>]*>(.*?)</html>", response_content, re.DOTALL | re.IGNORECASE)
    html_code = html_match.group(0).strip() if html_match else None

    # CSS 부분 추출
    css_match = re.search(r"<style>\n(.*?)</style>", response_content, re.DOTALL | re.IGNORECASE)
    css_code = css_match.group(0).strip() if css_match else None

    return html_code, css_code