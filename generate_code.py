# generate_code.py

import openai

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
