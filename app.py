import streamlit as st
import google.generativeai as genai
from tavily import TavilyClient

st.set_page_config(page_title="JARVIS SYSTEM", page_icon="🤖", layout="wide")

# Темная тема
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stTextInput>div>div>input { background-color: #1a1c24; color: white; border-color: #4f5b66; }
    .stButton>button { background-color: #00d2ff; color: black; font-weight: bold; width: 100%; border: none; height: 3em;}
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 СИСТЕМА ДЖАРВИС v3.2")

with st.sidebar:
    st.header("🔑 КЛЮЧИ ДОСТУПА")
    google_key = st.text_input("Google API Key:", type="password")
    tavily_key = st.text_input("Tavily API Key:", type="password")
    st.markdown("---")
    
    # Кнопка диагностики (если опять будет 404)
    if st.button("Проверить доступные модели"):
        if google_key:
            try:
                genai.configure(api_key=google_key.strip())
                models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                st.write("Твоему ключу доступны:")
                st.write(models)
            except Exception as e:
                st.error(f"Ошибка ключа: {e}")
        else:
            st.warning("Сначала введите ключ")

mode = st.radio("РЕЖИМ:", ["🔍 OSINT", "🎭 RP Mode"], horizontal=True)
user_query = st.text_area("ЗАПРОС:")

if st.button("ЗАПУСТИТЬ ПРОЦЕССОР"):
    if not google_key:
        st.error("Введите Google Key!")
    else:
        try:
            genai.configure(api_key=google_key.strip())
            
            # --- УМНЫЙ ПОДБОР МОДЕЛИ ---
            # Мы пробуем найти любую рабочую модель из списка доступных
            available_models = []
            try:
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        available_models.append(m.name)
            except:
                available_models = ['models/gemini-1.5-flash', 'models/gemini-pro']

            # Выбираем первую из списка или дефолтную
            target_model = available_models[0] if available_models else 'gemini-1.5-flash'
            model = genai.GenerativeModel(target_model)
            
            if mode == "🎭 RP Mode":
                with st.spinner(f"Использую {target_model}..."):
                    res = model.generate_content(f"Ты Джарвис, придумай досье: {user_query}")
                    st.markdown(res.text)
            else:
                if not tavily_key:
                    st.error("Нужен Tavily Key!")
                else:
                    with st.spinner(f"Сканирую через {target_model}..."):
                        tavily = TavilyClient(api_key=tavily_key.strip())
                        search = tavily.search(query=user_query, search_depth="advanced")
                        res = model.generate_content(f"Данные: {search}. Проанализируй связи для: {user_query}")
                        st.markdown(res.text)
                        
        except Exception as e:
            st.error(f"❌ СБОЙ: {str(e)}")
            st.info("Попробуйте создать НОВЫЙ ключ в Google AI Studio, возможно этот заблокирован.")
