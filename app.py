import streamlit as st
import google.generativeai as genai
from tavily import TavilyClient

st.set_page_config(page_title="JARVIS AI", page_icon="🤖", layout="wide")

st.title("🤖 СИСТЕМА ДЖАРВИС v3.6 (Resilient)")

with st.sidebar:
    st.header("🔑 ТЕРМИНАЛ")
    g_key = st.text_input("Google API Key:", type="password")
    t_key = st.text_input("Tavily API Key:", type="password")

mode = st.radio("РЕЖИМ:", ["🔍 OSINT", "🎭 RP Mode"], horizontal=True)
user_query = st.text_area("ЗАПРОС:")

def get_working_model():
    # Список всех возможных имен моделей, которые сейчас работают
    # Пробуем по порядку, от новых к старым
    test_names = [
        'gemini-1.5-flash-latest', 
        'gemini-1.5-flash', 
        'gemini-pro',
        'models/gemini-1.5-flash',
        'models/gemini-pro'
    ]
    
    for name in test_names:
        try:
            model = genai.GenerativeModel(name)
            # Проверочный микро-запрос
            model.generate_content("hi", generation_config={"max_output_tokens": 1})
            return model, name
        except:
            continue
    return None, None

if st.button("ЗАПУСТИТЬ ПРОЦЕССОР"):
    if not g_key.strip() or not t_key.strip():
        st.error("Введите оба ключа!")
    else:
        try:
            genai.configure(api_key=g_key.strip())
            
            # Ищем рабочую модель
            model, model_name = get_working_model()
            
            if not model:
                st.error("❌ Google отклоняет все модели. Попробуй создать НОВЫЙ ключ в Google AI Studio.")
            else:
                st.info(f"Система активна. Используется модуль: {model_name}")
                
                if mode == "🎭 RP Mode":
                    with st.spinner("Генерация..."):
                        res = model.generate_content(f"Ты Джарвис, придумай: {user_query}")
                        st.markdown(res.text)
                else:
                    with st.spinner("Поиск..."):
                        tavily = TavilyClient(api_key=t_key.strip())
                        search = tavily.search(query=user_query, search_depth="advanced")
                        res = model.generate_content(f"Данные: {search}. Анализ для: {user_query}")
                        st.markdown(res.text)
                        
        except Exception as e:
            st.error(f"❌ ОШИБКА: {str(e)}")
