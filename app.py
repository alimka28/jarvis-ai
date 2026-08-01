import streamlit as st
import google.generativeai as genai
from tavily import TavilyClient

st.set_page_config(page_title="JARVIS SYSTEM", layout="wide")
st.title("🤖 СИСТЕМА ДЖАРВИС v3.0")

with st.sidebar:
    st.header("⚙️ ТЕРМИНАЛ ДОСТУПА")
    google_key = st.text_input("ВВЕДИТЕ GOOGLE KEY:", type="password")
    tavily_key = st.text_input("ВВЕДИТЕ TAVILY KEY:", type="password")

mode = st.selectbox("ВЫБЕРИТЕ РЕЖИМ:", ["🔍 OSINT (Поиск по людям)", "🎭 RP Mode (Выдумка)"])
user_query = st.text_input("ВВЕДИТЕ ЗАПРОС:")

if st.button("ЗАПУСТИТЬ АНАЛИЗ"):
    if not google_key:
        st.error("Введите Google Key!")
    else:
        try:
            genai.configure(api_key=google_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            if mode == "🎭 RP Mode (Выдумка)":
                res = model.generate_content(f"Ты Джарвис. ПРИДУМАЙ: {user_query}")
                st.write(res.text)
            else:
                if not tavily_key:
                    st.error("Нужен Tavily Key!")
                else:
                    tavily = TavilyClient(api_key=tavily_key)
                    search = tavily.search(query=user_query, search_depth="advanced")
                    res = model.generate_content(f"Данные: {search}. Анализ: {user_query}")
                    st.write(res.text)
        except Exception as e:
            st.error(f"Ошибка: {e}")
