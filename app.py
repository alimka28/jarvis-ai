import streamlit as st
import google.generativeai as genai
from tavily import TavilyClient

# Настройка страницы
st.set_page_config(page_title="JARVIS AI", page_icon="🤖", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stTextInput>div>div>input { background-color: #1a1c24; color: white; }
    .stButton>button { background-color: #00d2ff; color: black; font-weight: bold; width: 100%; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 СИСТЕМА ДЖАРВИС v3.5")

with st.sidebar:
    st.header("🔑 ТЕРМИНАЛ")
    # Тщательно проверяем имена переменных!
    g_key = st.text_input("Google API Key:", type="password")
    t_key = st.text_input("Tavily API Key:", type="password")

mode = st.radio("РЕЖИМ:", ["🔍 OSINT (Поиск)", "🎭 RP Mode (Выдумка)"], horizontal=True)
user_query = st.text_area("ЗАПРОС:")

if st.button("ЗАПУСТИТЬ ПРОЦЕССОР"):
    # Проверка, что оба поля заполнены
    if not g_key.strip() or not t_key.strip():
        st.error("Ошибка: Введите ОБА ключа в боковой панели!")
    else:
        try:
            # Настраиваем Google
            genai.configure(api_key=g_key.strip())
            model = genai.GenerativeModel('gemini-1.5-flash')

            if mode == "🎭 RP Mode (Выдумка)":
                with st.spinner("Джарвис генерирует данные..."):
                    res = model.generate_content(f"Ты Джарвис, придумай досье для RP: {user_query}")
                    st.markdown(res.text)
            else:
                with st.spinner("Джарвис сканирует интернет..."):
                    # Исправлено: теперь используем t_key, который определен выше
                    tavily = TavilyClient(api_key=t_key.strip())
                    search = tavily.search(query=user_query, search_depth="advanced")
                    
                    prompt = f"Данные из интернета: {search}. Проанализируй связи для: {user_query}. Учти законы Украины."
                    res = model.generate_content(prompt)
                    st.markdown(res.text)
                        
        except Exception as e:
            st.error(f"❌ СБОЙ СИСТЕМЫ: {str(e)}")
