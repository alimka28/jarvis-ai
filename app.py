import streamlit as st
import google.generativeai as genai
from tavily import TavilyClient

st.title("🤖 JARVIS v4.0 (Easy Mode)")

# Упрощаем ввод: всё в одной колонке
g_key = st.text_input("Вставь Google Key:", type="password")
t_key = st.text_input("Вставь Tavily Key (необязательно):", type="password")
query = st.text_area("Твой вопрос:")

if st.button("ЗАПУСК"):
    if not g_key:
        st.error("Без Google Key я не смогу думать!")
    else:
        try:
            genai.configure(api_key=g_key.strip())
            # Пробуем самую простую модель без лишних слов
            model = genai.GenerativeModel('gemini-pro') 
            
            # Если есть ключ Tavily и запрос сложный — ищем. Иначе — просто отвечаем.
            if t_key.strip() and len(query) > 5:
                try:
                    tavily = TavilyClient(api_key=t_key.strip())
                    search = tavily.search(query=query)
                    final_prompt = f"Данные из сети: {search}\n\nВопрос: {query}"
                    st.info("🔍 Использовал поиск")
                except:
                    final_prompt = query
                    st.warning("⚠️ Поиск не сработал, отвечаю из памяти")
            else:
                final_prompt = query

            response = model.generate_content(final_prompt)
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"Бро, опять ошибка: {e}")
                        
        except Exception as e:
            st.error(f"❌ ОШИБКА: {str(e)}")
