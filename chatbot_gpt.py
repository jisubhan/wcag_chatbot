import openai
import streamlit as st
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader
import os

# .env 파일에서 OpenAI API 키 로드
load_dotenv()

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

# 'guide.pdf' 파일을 data 디렉토리에서 로드
pdf_file_path = "data/wcag.pdf"

# 'wcag.txt' 파일을 data 디렉토리에서 로드
txt_file_path = "data/long.txt"

# 벡터 스토어 디렉토리 경로 생성
vector_store_dir = os.path.join(os.getcwd(), os.path.splitext(os.path.basename(pdf_file_path))[0])

# 벡터 스토어가 이미 존재하는지 확인하고, 존재하면 로드
def load_vector_store(directory):
    faiss_index_path = os.path.join(directory,"index.faiss")
    print("faiss_index_path="+faiss_index_path)
    if os.path.exists(faiss_index_path):
        st.write(f"벡터 스토어가 이미 존재합니다: {faiss_index_path}")
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
def generate_code(prompt, code, guidelines):
    full_prompt = f"""
당신은 웹 접근성 전문가입니다. 아래의 웹 콘텐츠 접근성 지침 요약을 참고하여, 사용자가 제공한 HTML 코드를 '{prompt}' 요청에 따라 수정하세요.

웹 콘텐츠 접근성 지침 요약:
{guidelines}

사용자 제공 코드:
{code}

수정된 코드만 제공하세요.
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

def generate_explanation(original_code, modified_code, relevant_text):
    explanation_prompt = f"""
    다음은 사용자가 제공한 원본 코드입니다.\n원본 코드:{original_code}\n그리고 다음은 수정된 코드입니다.\n수정된 코드:{modified_code}\n
    "웹접근성지침"으로 {relevant_text}를 정리해서 출력하고 이후 수정 사항을 간략히 설명해주세요.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": explanation_prompt}],
        max_tokens=500,
        temperature=0,
        n=1,
        stop=None,
    )
    explanation = response.choices[0].message.content.strip()
    return explanation