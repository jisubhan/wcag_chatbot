# generate_explanation.py

import openai

def generate_explanation(original_code, modified_code):
    explanation_prompt = f"""
다음은 사용자가 제공한 원본 코드입니다:

원본 코드:
{original_code}

그리고 다음은 수정된 코드입니다:

수정된 코드:
{modified_code}

수정 사항을 간략히 설명해주세요.
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
