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

st.title("🤖 СИСТЕМА ДЖАРВИС v3.3")

with st.sidebar:
    st.header("🔑 ТЕРМИНАЛ")
    google_key = st.text_input("Google API Key:", type="password")
    tavily_key = st.text_input("Tavily API Key:", type="password")
    st.info("Введите ключи и начните работу.")

mode = st.radio("РЕЖИМ:", ["🔍 OSINT (Поиск)", "🎭 RP Mode (Выдумка)"], horizontal=True)
user_query = st.text_area("ЗАПРОС:")

if st.button("ЗАПУСТИТЬ ПРОЦЕССОР"):
    if not google_key:
        st.error("Ошибка: Введите Google Key")
    else:
        try:
            # Настраиваем Google
            genai.configure(api_key=google_key.strip())
            
            # --- ЖЕСТКИЙ ВЫБОР МОДЕЛИ ---
            # Пробуем по очереди самые стабильные варианты
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                # Тестовый микровзброс, чтобы проверить, жива ли модель
                _ = model.generate_content("hi") 
            except:
                try:
                    model = genai.GenerativeModel('gemini-1.5-pro')
                    _ = model.generate_content("hi")
                except:
                    model = genai.GenerativeModel('gemini-pro')

            if mode == "🎭 RP Mode (Выдумка)":
                with st.spinner("Джарвис генерирует..."):
                    res = model.generate_content(f"Ты Джарвис, придумай досье для RP: {user_query}")
                    st.markdown(res.text)
            else:
                if not tavily_key:
                    st.error("Ошибка: Нужен Tavily Key")
                else:
                    with st.spinner("Джарвис сканирует интернет..."):
                        tavily = TavilyClient(api_key=tavily_key.strip())
                        search = tavily.search(query=user_query, search_depth="advanced")
                        res = model.generate_content(f"Данные из интернета: {search}. Проанализируй связи и события для: {user_query}. Учти законы Украины.")
                        st.markdown(res.text)
                        
        except Exception as e:
            st.error(f"❌ ОШИБКА ДОСТУПА: {str(e)}")
            st.warning("Если вы видите 404, ваш API-ключ не активирован для этих моделей. Попробуйте создать НОВЫЙ ключ в Google AI Studio.")
