import streamlit as st
import openai
import requests
from bs4 import BeautifulSoup

# Установка API-ключа OpenAI
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="ИИ-прескоринг кандидатов", layout="centered")
st.title("🔍 ИИ-прескоринг кандидатов")

st.markdown("Введите **несколько** ссылок на резюме и одну ссылку на вакансию с hh.ru")

resume_urls = st.text_area("Ссылки на резюме (по одной в строке)").strip().split("\n")
vacancy_url = st.text_input("Ссылка на вакансию:")

if st.button("Анализировать кандидатов"):
    if not resume_urls or not vacancy_url:
        st.error("❗ Укажите как минимум одну ссылку на резюме и ссылку на вакансию.")
        st.stop()

    def extract_text_from_hh(url):
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text(separator='\n')
            return text.strip()
        except Exception as e:
            return f"[Ошибка при извлечении: {e}]"

    with st.spinner("🔎 Извлечение текста со страниц hh.ru..."):
        resumes = [extract_text_from_hh(url) for url in resume_urls if url.strip()]
        vacancy = extract_text_from_hh(vacancy_url)

    with st.spinner("🤖 Анализируем кандидатов GPT-4.1..."):
        prompt = f"""
Ты помощник по подбору персонала. Ниже приведена вакансия и список резюме.
Твоя задача — определить, какой из кандидатов наиболее подходит под вакансию и почему.
Дай краткую сравнительную оценку по ключевым навыкам и опытам, выдели сильные/слабые стороны.
В конце сделай заключение: кого бы ты рекомендовал в первую очередь.

Вакансия:
=====
{vacancy}

Резюме:
"""
        for i, resume in enumerate(resumes, 1):
            prompt += f"\n---\nКандидат {i}:\n{resume}\n"

        response = openai.chat.completions.create(
            model="gpt-4-1106-preview",  # GPT-4.1
            messages=[
                {"role": "system", "content": "Ты опытный HR-аналитик."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        result = response.choices[0].message.content

    st.success("✅ Анализ завершён!")
    st.markdown("### 🧠 Результат анализа:")
    st.markdown(result)
