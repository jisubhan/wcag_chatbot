# 🧑🏻‍💻 웹 콘텐츠 수정 자동화 서비스

## 🚀 프로젝트 소개

- 이 웹 서비스는 한국형 웹 콘텐츠 접근성 지침을 준수하여 개발된 자동화된 코드 수정 서비스입니다.
- 사용자는 HTML 및 CSS 코드를 입력하고, 웹 접근성 지침에 따라 코드를 수정하거나 생성할 수 있습니다.
- 이 서비스는 인공지능을 활용하여 코드의 접근성을 자동으로 개선합니다.

<br>

## ✨팀원 구성

<div align="center">

| **손현열** | **김용운** | **김신호** | **한지섭** |
| :------: |  :------: | :------: | :------: |
| [<img src="https://github.com/user-attachments/assets/9db34279-78a5-4a60-b0e5-b5930b81e01e" height=150 width=150> <br/> @sonhyunheol](https://github.com/jisubhan) | [<img src="https://github.com/user-attachments/assets/b1e9b2b0-d620-4cea-b03d-62296e6e81e4" height=150 width=150> <br/> @kimyongwoon](https://github.com/jisubhan) | [<img src="https://github.com/user-attachments/assets/9c2fc040-9b18-4cfa-bb77-c5a73ce3b68a" height=150 width=150> <br/> @kimsh](https://github.com/jisubhan) | [<img src="https://github.com/user-attachments/assets/7fb33fee-7166-4067-b9d7-5804b6b4d451" height=150 width=150> <br/> @jisubhan](https://github.com/jisubhan) |

</div>

<br>

## 설치 방법
필수 조건
- Python 3.7 이상
- OpenAI API 키
- Git (선택 사항)
설치 단계


### 리포지토리 클론

bash


코드 복사
git clone https://github.com/jisubhan/wcag_chatbot.git
cd your-repo-name
가상 환경 생성 (선택 사항)
<br>
bash
코드 복사
python -m venv venv
source venv/bin/activate  # Windows의 경우 'venv\Scripts\activate'
필요한 패키지 설치
<br>
bash
코드 복사
pip install -r requirements.txt
환경 변수 설정
<br>
프로젝트 루트 디렉터리에 .env 파일을 생성하고, OpenAI API 키를 추가합니다.
<br>
env
코드 복사
OPENAI_API_KEY="open_api_key"
웹 접근성 지침 요약 파일 준비

data/wcag.txt 파일이 있는지 확인하세요. 없을 경우, 한국형 웹 콘텐츠 접근성 지침의 주요 내용을 요약하여 해당 위치에 저장합니다.

사용 방법
애플리케이션 실행

bash
코드 복사
streamlit run chatbot.py
웹 브라우저에서 접속

터미널에 표시된 로컬 URL을 웹 브라우저에 입력하여 애플리케이션에 접속합니다.

## 코드 입력 및 수정

- 코드 편집기에 수정하고자 하는 HTML 코드를 입력합니다.
- 아래의 '코드 수정 요청' 입력란에 원하는 수정 요청을 입력합니다.
- 예: "웹 접근성 문제를 해결해줘"
- '✨ 코드 생성/수정' 버튼을 클릭합니다.
- 수정된 코드 확인 및 미리보기

- 수정된 코드와 차이점 섹션에서 원본 코드와 수정된 코드의 차이점을 시각적으로 비교합니다.
- 수정된 코드 웹에서 확인하기 섹션에서 수정된 코드를 실제 웹 페이지로 미리볼 수 있습니다.
- 수정 사항 설명 섹션에서 AI가 제공한 수정 내용을 확인합니다.

## ⏱️ 개발 기간 및 작업 관리

### 🖥️ 개발 기간

- 전체 개발 기간 : 2024-09-13 ~ 2024-10-25
- 프론트엔드 구현 : 2024-09-20 ~ 2024-10-18
- 데이터 모델 및 백엔드 구현 : 2024-09-20 ~ 2024-10-18


### ⚙️ 작업 관리

- GitHub와 Confluence 및 Jira Issues를 사용하여 진행 상황을 공유했습니다.
- 주간 스크럼을 진행하며 작업 순서와 방향성에 대한 고민을 나누고 Jira에 ISSUE 내용을 기록했습니다.

<br>

## 👀프로젝트 구조

```
WCAG_CHATBOT/
├── chatbot_gpt.py               # api 연동 모듈
├── streamlit_pdf.py             # 메인 실행 모듈
├── requirements.txt             # 필요한 패키지 목록
├── .env                         # api KEY
├── data/
│   └── wcag.txt                 # 웹 접근성 지침 요약본
│   └── wcag.pdf                 # 웹 접근성 지침 
├── wcag/
│   └── index.faiss              # faiss
│   └── index.pkl                
├── assets/
│   └── banner.png               # README에 사용된 이미지
└── README.md                    # 프로젝트 설명 파일
```

## 🚩 사용 라이브러리 목록
### 💡 라이브러리 이름 목적 및 기능
- OpenAI	: OpenAI API를 이용한 자연어 처리 및 생성 작업
- Streamlit	: 웹 애플리케이션 개발을 위한 프레임워크
- python-dotenv	: .env 파일을 통해 환경 변수 로드 및 관리
- LangChain_OpenAIEmbeddings : OpenAI의 임베딩 기능을 활용한 텍스트 벡터화
- LangChain_FAISS : FAISS를 이용한 벡터 스토어 관리 및 검색
- LangChain_RecursiveCharacterTextSplitter : 텍스트를 재귀적으로 분할하여 처리
- PyPDF2 : PDF 파일 읽기 및 처리
- streamlit_ace	: 코드 편집기 기능 제공을 위한 Streamlit 모듈
- tinycss2	: CSS 파일 파싱 및 분석
- difflib	: 텍스트 및 코드의 비교 및 차이점 분석


## 📌 주요 기능
- 코드 편집기 제공: ACE Editor를 통해 HTML 코드를 직접 입력 및 수정할 수 있습니다.
- 자동 코드 수정: 웹 접근성 지침에 따라 코드를 자동으로 수정합니다.
- 수정 사항 비교: 원본 코드와 수정된 코드의 차이점을 시각적으로 비교하여 보여줍니다.
- 미리보기 기능: 수정된 코드를 웹 환경에서 실시간으로 미리볼 수 있습니다.
- 다크 모드 지원: 다크 모드에서도 가독성이 유지되도록 디자인되었습니다.
- 수정 사항 설명: AI가 제공하는 수정 사항 설명을 통해 변경된 내용을 쉽게 이해할 수 있습니다.
- 예시 질문 제공: 웹 접근성 개선에 도움이 되는 예시 질문을 제공합니다.
<br>



