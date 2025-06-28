# streamlit_app.py

import streamlit as st
from openai import OpenAI
from parse_hh import get_text_from_hh

# Настройка ключа
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Анализ резюме и вакансии", layout="wide")
st.title("🔍 ИИ-ассистент для прескоринга кандидатов")

st.markdown("Введите ссылки на резюме и вакансию с hh.ru")

resume_url = st.text_input("Ссылка на резюме:")
vacancy_url = st.text_input("Ссылка на вакансию:")

if st.button("Анализировать"):
    try:
        resume_text = get_text_from_hh(resume_url)
        vacancy_text = get_text_from_hh(vacancy_url)

        with st.spinner("⚙️ Обращение к OpenAI..."):
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Ты опытный HR-ассистент. Сравни резюме кандидата с вакансией и оцени:\n"
                            "- Насколько кандидат подходит на вакансию (по 10-бальной шкале)\n"
                            "- Соответствие по ключевым навыкам\n"
                            "- Есть ли критичные несоответствия\n"
                            "- Дай рекомендации работодателю"
                        )
                    },
                    {"role": "user", "content": f"Вакансия:\n{vacancy_text}"},
                    {"role": "user", "content": f"Резюме:\n{resume_text}"}
                ]
            )

            st.success("✅ Анализ завершён!")
            st.markdown("### 📊 Результат анализа:")
            st.write(response.choices[0].message.content)

    except Exception as e:
        st.error(f"Ошибка: {str(e)}")