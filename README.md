# 🧑🏻‍💻 웹 콘텐츠 수정 자동화 챗봇

## 프로젝트 소개

- 이 웹 서비스는 한국형 웹 콘텐츠 접근성 지침을 준수하여 개발된 자동화된 코드 수정 서비스입니다.
- 사용자는 HTML 및 CSS 코드를 입력하고, 웹 접근성 지침에 따라 코드를 수정하거나 생성할 수 있습니다.
- 이 서비스는 인공지능을 활용하여 코드의 접근성을 자동으로 개선합니다.

<br>

## 팀원 구성

<div align="center">
| **손현열** | **김신호** | **김용운** | **한지섭** |
| :------: |  :------: | :------: | :------: |
| [<img src="https://github.com/user-attachments/assets/9db34279-78a5-4a60-b0e5-b5930b81e01e" height=150 width=150>  | [<img src="![shy](https://github.com/user-attachments/assets/e85e98d3-124a-4d5a-b43a-fd52effb8879)" height=150 width=150> | [<img src="![shy](https://github.com/user-attachments/assets/e85e98d3-124a-4d5a-b43a-fd52effb8879)" height=150 width=150> | [<img src="![shy](https://github.com/user-attachments/assets/e85e98d3-124a-4d5a-b43a-fd52effb8879)" height=150 width=150>  |

<div align="center">

| **손현열** | **김신호** | **김용운** | **한지섭** |
| :------: |  :------: | :------: | :------: |
| [<img src="[https://avatars.githubusercontent.com/u/106502312?v=4](https://github.com/user-attachments/assets/9db34279-78a5-4a60-b0e5-b5930b81e01e)" height=150 width=150> <br/> @yeon1615](https://github.com/yeon1615) | [<img src="https://avatars.githubusercontent.com/u/112460466?v=4" height=150 width=150> <br/> @Cheorizzang](https://github.com/Cheorizzang) | [<img src="https://avatars.githubusercontent.com/u/112460506?v=4" height=150 width=150> <br/> @heejiyang](https://github.com/heejiyang) | [<img src="https://avatars.githubusercontent.com/u/76766459?v=4" height=150 width=150> <br/> @journey-ji](https://github.com/journey-ji) |

</div>

</div>

<br>

## 1. 주요 기능
- 코드 편집기 제공: ACE Editor를 통해 HTML 코드를 직접 입력 및 수정할 수 있습니다.
- 자동 코드 수정: 웹 접근성 지침에 따라 코드를 자동으로 수정합니다.
- 수정 사항 비교: 원본 코드와 수정된 코드의 차이점을 시각적으로 비교하여 보여줍니다.
- 미리보기 기능: 수정된 코드를 웹 환경에서 실시간으로 미리볼 수 있습니다.
- 다크 모드 지원: 다크 모드에서도 가독성이 유지되도록 디자인되었습니다.
- 수정 사항 설명: AI가 제공하는 수정 사항 설명을 통해 변경된 내용을 쉽게 이해할 수 있습니다.
- 예시 질문 제공: 웹 접근성 개선에 도움이 되는 예시 질문을 제공합니다.
<br>

##  프로젝트 구조

```
WCAG_CHATBOT/
├── chatbot_gpt.py               # api 연동 모듈
├── streamlit_pdf.py             # 메인 실행 모듈
├── generate_code.py             # 코드 생성을 위한 모듈
├── generate_explanation.py      # 수정 사항 설명 생성을 위한 모듈
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

    
<br>

## 개발 기간 및 작업 관리

### 개발 기간

- 전체 개발 기간 : 2024-09-13 ~ 2024-10-25
- 프론트엔드 구현 : 2024-09-20 ~ 2024-10-18
- 데이터 모델 및 백엔드 구현 : 2024-09-20 ~ 2024-10-18

<br>

### 작업 관리

- GitHub와 Confluence 및 Jira Issues를 사용하여 진행 상황을 공유했습니다.
- 주간 스크럼을 진행하며 작업 순서와 방향성에 대한 고민을 나누고 Jira에 ISSUE 내용을 기록했습니다.

<br>

