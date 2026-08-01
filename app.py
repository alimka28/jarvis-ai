import streamlit as st
import google.generativeai as genai
from tavily import TavilyClient

# --- НАСТРОЙКА ИНТЕРФЕЙСА ---
st.set_page_config(page_title="JARVIS SYSTEM", page_icon="🤖", layout="wide")

# Кастомный темный стиль "Джарвис"
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stTextInput>div>div>input { background-color: #1a1c24; color: white; border-color: #4f5b66; }
    .stButton>button { background-color: #00d2ff; color: black; font-weight: bold; width: 100%; border: none; }
    .stButton>button:hover { background-color: #00a8cc; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 СИСТЕМА ДЖАРВИС v3.1")
st.write("---")

# --- БОКОВАЯ ПАНЕЛЬ ---
with st.sidebar:
    st.header("🔑 КЛЮЧИ ДОСТУПА")
    google_key = st.text_input("Google API Key:", type="password", help="Из Google AI Studio")
    tavily_key = st.text_input("Tavily API Key:", type="password", help="Из Tavily Dashboard")
    st.markdown("---")
    st.info("Система готова к работе. Все запросы проходят через зашифрованный туннель.")

# --- ОСНОВНОЙ ИНТЕРФЕЙС ---
col1, col2 = st.columns([2, 1])

with col1:
    mode = st.radio("ВЫБЕРИТЕ РЕЖИМ:", ["🔍 OSINT (Поиск связей по миру)", "🎭 RP Mode (Ролевая игра/Выдумка)"], horizontal=True)
    user_query = st.text_area("ВВЕДИТЕ ЗАПРОС ИЛИ ИМЯ ОБЪЕКТА:", placeholder="Например: 'Индира Ганди, связи с секретными организациями' или 'Придумай досье на киборга'...")

# --- ЛОГИКА РАБОТЫ ---
if st.button("ЗАПУСТИТЬ ПРОЦЕССОР"):
    if not google_key:
        st.error("❌ ОШИБКА: Отсутствует Google API Key. Система не может 'думать'.")
    else:
        try:
            # Настройка Google AI
            genai.configure(api_key=google_key.strip())
            
            # Пытаемся подключить модель (с запасным вариантом, если 1.5-flash недоступна)
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                test_check = model.generate_content("test") # Проверка работоспособности
            except:
                model = genai.GenerativeModel('gemini-pro')

            # --- РЕЖИМ RP ---
            if mode == "🎭 RP Mode (Выдумка/Ролевая)":
                with st.spinner("ГЕНЕРАЦИЯ ВООВРАЖАЕМЫХ ДАННЫХ..."):
                    prompt = f"Ты — Джарвис. ПРИДУМАЙ детальное творческое досье или историю по запросу: {user_query}. Будь креативен, создавай интриги и связи."
                    response = model.generate_content(prompt)
                    st.success("🎭 ДОСЬЕ СФОРМИРОВАНО:")
                    st.markdown(response.text)

            # --- РЕЖИМ OSINT ---
            else:
                if not tavily_key:
                    st.error("❌ ОШИБКА: Для поиска нужен Tavily API Key.")
                else:
                    with st.spinner("СКАНИРОВАНИЕ ГЛОБАЛЬНОЙ СЕТИ..."):
                        tavily = TavilyClient(api_key=tavily_key.strip())
                        # Глубокий поиск
                        search_results = tavily.search(query=user_query, search_depth="advanced")
                        
                        prompt = f"""
                        Ты — Джарвис, эксперт по OSINT и безопасности. 
                        Твоя задача — проанализировать данные: {search_results}
                        Запрос пользователя: {user_query}
                        
                        ИНСТРУКЦИИ:
                        1. Найди все факты об объекте/событии.
                        2. Выяви скрытые СВЯЗИ с другими людьми или организациями.
                        3. Составь список совпадений (Граф связей).
                        4. Проверь законность действий по законам Украины (пользователю 17 лет).
                        5. Формат отчета: Лаконично, четко, только по делу.
                        """
                        response = model.generate_content(prompt)
                        st.success("🔍 ОТЧЕТ АНАЛИТИЧЕСКОЙ СИСТЕМЫ:")
                        st.markdown(response.text)

        except Exception as e:
            st.error(f"⚠️ КРИТИЧЕСКИЙ СБОЙ: {str(e)}")
            st.info("Совет: Проверьте правильность API ключей и наличие интернета.")

st.write("---")
st.caption("Jarvis AI Terminal © 2024. Все данные берутся из открытых легальных источников.")
