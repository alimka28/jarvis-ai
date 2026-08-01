import streamlit as st
from openai import OpenAI
from tavily import TavilyClient

st.set_page_config(page_title="JARVIS v4.0", page_icon="🤖", layout="wide")

st.title("🤖 JARVIS: OPENROUTER EDITION")

# Настройки в боковой панели
with st.sidebar:
    st.header("🔑 ТЕРМИНАЛ КЛЮЧЕЙ")
    or_key = st.text_input("OpenRouter API Key:", type="password")
    tv_key = st.text_input("Tavily API Key:", type="password")
    st.markdown("---")
    st.write("Система использует OpenRouter для обхода блокировок Google.")

mode = st.radio("РЕЖИМ:", ["🔍 OSINT (Поиск)", "🎭 RP Mode (Выдумка)"], horizontal=True)
user_query = st.text_input("ВАШ ЗАПРОС:")

if st.button("ВЫПОЛНИТЬ"):
    if not or_key:
        st.error("Введите OpenRouter Key!")
    else:
        try:
            # Настройка клиента OpenRouter
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=or_key.strip(),
            )

            # Выбор модели (бесплатная и мощная)
            # Можно заменить на "google/gemini-flash-1.5:free", если хочешь именно Gemini
            selected_model = "meta-llama/llama-3.1-8b-instruct:free"

            if mode == "🔍 OSINT (Поиск)":
                if not tv_key:
                    st.error("Нужен Tavily Key для поиска!")
                else:
                    with st.spinner("Джарвис сканирует сеть..."):
                        tavily = TavilyClient(api_key=tv_key.strip())
                        search_data = tavily.search(query=user_query, search_depth="advanced")
                        
                        prompt = f"Данные поиска: {search_data}. Проанализируй связи для: {user_query}. Учти законы Украины."
                        
                        response = client.chat.completions.create(
                            model=selected_model,
                            messages=[{"role": "user", "content": prompt}]
                        )
                        st.markdown(response.choices[0].message.content)
            
            else: # Режим RP
                with st.spinner("Джарвис генерирует..."):
                    prompt = f"Ты Джарвис, придумай творческое досье/историю: {user_query}"
                    response = client.chat.completions.create(
                        model=selected_model,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    st.markdown(response.choices[0].message.content)

        except Exception as e:
            st.error(f"Ошибка: {str(e)}")

st.caption("Powered by OpenRouter & Tavily")
