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

st.title("🤖 СИСТЕМА ДЖАРВИС v3.4")

with st.sidebar:
    st.header("🔑 ТЕРМИНАЛ")
    # Используй strip() чтобы убрать случайные пробелы при вставке
    g_key = st.text_input("Google API Key:", type="password")
    t_key = st.text_input("Tavily API Key:", type="password")

mode = st.radio("РЕЖИМ:", ["🔍 OSINT (Поиск)", "🎭 RP Mode (Выдумка)"], horizontal=True)
user_query = st.text_area("ЗАПРОС:")

if st.button("ЗАПУСТИТЬ ПРОЦЕССОР"):
    if not g_key or not t_key:
        st.error("Ошибка: Введите ОБА ключа (Google и Tavily)")
    else:
        try:
            # Настраиваем Google
            genai.configure(api_key=g_key.strip())
            
            # Используем САМУЮ проверенную модель. Без вариантов.
            model = genai.GenerativeModel('gemini-1.5-flash')

            if mode == "🎭 RP Mode (Выдумка)":
                with st.spinner("Джарвис генерирует данные..."):
                    res = model.generate_content(f"Ты Джарвис, придумай досье для RP: {user_query}")
                    st.markdown(res.text)
            else:
                with st.spinner("Джарвис сканирует интернет..."):
                    tavily = TavilyClient(api_key=tavily_key.strip())
                    search = tavily.search(query=user_query, search_depth="advanced")
                    res = model.generate_content(f"Данные из интернета: {search}. Проанализируй связи для: {user_query}. Учти законы Украины.")
                    st.markdown(res.text)
                        
        except Exception as e:
            st.error(f"❌ СБОЙ: {str(e)}")
