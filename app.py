import streamlit as st
import altair as alt
import pandas as pd
import json
from y import find_best_cities, load_cities_from_json, calculate_similarity, categorize_infrastructure, categorize_greenery

# Настройки страницы
st.set_page_config(page_title="Выбор города", page_icon="🏙️", layout="wide")

# Боковая панель: информация
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/684/684908.png", width=100)
    st.markdown("## 🌇 Выбор города")
    st.markdown(
        "Этот сайт помогает подобрать **наиболее комфортный город** в России "
        "на основе **ваших предпочтений** по климату, инфраструктуре, ритму жизни и другим факторам."
    )
    st.markdown("---")
    st.markdown("Разработано в рамках курсовой работы.")

# Основной заголовок
st.title("🏡 Найдите свой идеальный город")

# Загружаем данные
cities = load_cities_from_json("cities.json")

# Ввод предпочтений пользователя
with st.form("preferences_form"):
    st.subheader("Укажите ваши предпочтения")

    col1, col2, col3 = st.columns(3)

    with col1:
        climate = st.selectbox("Климат", [1, 2, 3], format_func=lambda x: ["Холодный", "Умеренный", "Жаркий"][x-1])
        weather_stability = st.selectbox("Стабильность погоды", [1, 2, 3], format_func=lambda x: ["Не важно", "Средняя", "Избегаю перепадов"][x-1])
        population = st.selectbox("Размер города", [1, 2, 3], format_func=lambda x: ["До 500 тыс.", "500 тыс. – 1 млн", "Более 1 млн"][x-1])
        city_rhythm = st.selectbox("Городской ритм", [1, 2, 3], format_func=lambda x: ["Спокойный", "Умеренный", "Оживлённый"][x-1])

    with col2:
        infrastructure = st.slider("Доступность инфраструктуры", 1, 10, 5)
        greenery = st.slider("Уровень озеленения", 1, 10, 5)
        safety = st.slider("Уровень безопасности", 1, 10, 5)
        cultural_activities = st.slider("Социальная и культурная активность", 1, 10, 5)

    with col3:
        work_mode = st.multiselect("Формат работы", [1, 2, 3], default=[1, 2], format_func=lambda x: ["Удалёнка", "Наём", "Свой бизнес"][x-1])
        lifestyle = st.multiselect("Образ жизни", [1, 2, 3], default=[2], format_func=lambda x: ["Активный", "Сидячий", "Средний"][x-1])
        preferred_objects = st.multiselect("Инфраструктура", [1, 2, 3, 4], default=[1, 3], format_func=lambda x: ["Базовые услуги", "Культура", "Транспорт", "Медицина"][x-1])
        green_preference = st.selectbox("Озеленение важнее всего в", [1, 2, 3], format_func=lambda x: ["Парках центра", "Природе за городом", "Общей экологии"][x-1])

    submitted = st.form_submit_button("🔍 Подобрать города")

if submitted:
# Обновляем предпочтения в session_state
    st.session_state.user_prefs = {
        "climate": climate,
        "weather_stability": weather_stability,
        "population": population,
        "city_rhythm": city_rhythm,
        "infrastructure": categorize_infrastructure(infrastructure),
        "greenery": categorize_greenery(greenery),
        "safety": safety,
        "cultural_activities": cultural_activities,
        "work_mode": work_mode,
        "lifestyle": lifestyle,
        "preferred_objects": preferred_objects,
        "green_preference": green_preference
    }

    # Категоризируем параметры
    user_prefs = st.session_state.user_prefs


  
    city_scores = [(city, calculate_similarity(city, user_prefs)) for city in cities]
    city_scores.sort(key=lambda x: x[1])
    recommended = city_scores[:5]

    if recommended:
        st.success(f"🔎 Найдено {len(recommended)} наиболее подходящих городов:")
    
        for city, score in recommended:
            with st.container():
                st.markdown("----")
                st.markdown(f"### 🏙️ {city['name']}")
                with st.expander("ℹ️ Подробнее"):
                    st.markdown(f"**📍 Население:** {'До 500 тыс.' if city['population'] == 1 else '500 тыс. – 1 млн' if city['population'] == 2 else 'Более 1 млн'}")
                    st.markdown(f"**🌡️ Климат:** {['Холодный', 'Умеренный', 'Жаркий'][city['climate'] - 1]}")
                    st.markdown(f"**🏗️ Инфраструктура:** {city['infrastructure']} / 3")
                    st.markdown(f"**🌳 Озеленение:** {city['greenery']} / 3")
                    st.markdown(f"**🛡️ Безопасность:** {city['safety']} / 10")
                    st.markdown(f"**🎭 Культура и активность:** {city['cultural_activities']} / 10")
        # Подготовка данных для графика
        score_data = pd.DataFrame({
            "Город": [city["name"] for city, _ in recommended],
            "Схожесть (чем меньше, тем лучше)": [score for _, score in recommended]})

        # Пояснение
        st.subheader("📊 Рейтинг рекомендованных городов по уровню соответствия")
        st.markdown("""
        На графике вы можете увидеть соответствие каждого города и баллов, которые он получил в процессе выполнения алгоритма.
        Вам стоит ориентироваться на факт: "**Чем ниже балл-тем выше соответствие города вашим предпочтениям**".
        С учётом всех указанных характеристик предложенные вам города из списка всех возможных оптимально подходят под заданные критерии. 
        """)

        # График (вертикальный)
        chart = alt.Chart(score_data).mark_bar(color="#4C72B0").encode(
            x=alt.X("Схожесть (чем меньше, тем лучше):Q", title="Баллы (меньше = лучше)"),
            y=alt.Y("Город:N", sort="-x"),
            tooltip=["Город", "Схожесть (чем меньше, тем лучше)"]).properties(height=300)
        st.altair_chart(chart, use_container_width=True)
            
    else:
        st.warning("К сожалению, подходящих городов не найдено.")

