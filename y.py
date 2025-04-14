import json

# Категоризация характеристик
def categorize_population(value):
    """Категоризация размера города по населению (в миллионах)."""
    if value <= 0.5:
        return 1
    elif 0.5 < value <= 1:
        return 2
    else:
        return 3

def categorize_infrastructure(value):
    """Категоризация уровня инфраструктуры."""
    if value <= 4:
        return 1
    elif 5 <= value <= 7:
        return 2
    else:
        return 3

def categorize_greenery(value):
    """Категоризация уровня озеленения."""
    if value <= 4:
        return 1
    elif 5 <= value <= 7:
        return 2
    else:
        return 3

def categorize_cultural_activities(value):
    """Категоризация социальной активности."""
    if value <= 4:
        return 1
    elif 5 <= value <= 7:
        return 2
    else:
        return 3
    
print("Эта программа поможет вам выбрать подходящие для вас\nгорода в соответствии с вашими предпочтениями.\nПожалуйста, ответьте на вопросы ниже в соответсвии с требованиями.\nПосле ответа первый вопрос и последующие нажимайте Enter\nи переходите к следующему вопросу.\nУспешного прохождения!")

# Загрузка данных из JSON файла
def load_cities_from_json(json_file_path):
    """Загрузка списка городов из JSON файла."""
    with open(json_file_path, 'r', encoding='utf-8') as file:
        return json.load(file)
    
# Сбор данных о предпочтениях пользователя
def get_user_preferences():
    """Сбор данных от пользователя с проверкой ввода и установкой значений по умолчанию."""
    try:
        work_mode = input("Выберите подходящий формат работы (1 - удалённая работа, 2 - работа в найме, 3 - свой бизнес; можно выбрать несколько, через запятую): ").split(',')
        work_mode = [int(option.strip()) for option in work_mode if option.strip().isdigit()]
        if not work_mode:
            work_mode = [1, 2, 3]

        lifestyle = input("Выберите ваш образ жизни (1 - активный, 2 - сидячий, 3 - средний; можно выбрать несколько, через запятую): ").split(',')
        lifestyle = [int(option.strip()) for option in lifestyle if option.strip().isdigit()]
        if not lifestyle:
            lifestyle = [1, 2]

        climate = int(input("Предпочитаемый климат (1 - холодный, 2 - умеренный, 3 - жаркий): "))
        weather_stability = int(input("Насколько важна стабильность погоды? (1 - неважно, 2 - средняя стабильность, 3 - избегаю резких перепадов): "))

        population = int(input("Предпочитаемый размер города (1 - до 500 тыс., 2 - 500 тыс. - 1 млн, 3 - более 1 млн): "))
        city_rhythm = int(input("Какой городской ритм вам комфортен? (1 - спокойный, 2 - умеренный, 3 - оживленный): "))

        infrastructure = int(input("Насколько важна доступность инфраструктуры? (1-10): "))
        preferred_objects = input("Какие объекты инфраструктуры важны? (1 - базовые услуги, 2 - культурные учреждения, 3 - транспорт, 4 - медицина; можно выбрать несколько, через запятую): ").split(',')
        preferred_objects = [int(option.strip()) for option in preferred_objects if option.strip().isdigit()]
        if not preferred_objects:
            preferred_objects = [1, 2, 3, 4]

        greenery = int(input("Насколько важно озеленение города? (1-10): "))
        green_preference = int(input("Что важнее? (1 - парки в центре, 2 - природа за городом, 3 - общая экология): "))

        safety = int(input("Насколько важен уровень безопасности? (1-10): "))
        cultural_activities = int(input("Как важна социальная активность и культурные мероприятия? (1-10): "))

        return {
            "climate": climate,
            "weather_stability": weather_stability,
            "population": population,
            "city_rhythm": city_rhythm,
            "infrastructure": categorize_infrastructure(infrastructure),
            "greenery": categorize_greenery(greenery),
            "work_mode": work_mode,
            "lifestyle": lifestyle,
            "preferred_objects": preferred_objects,
            "safety": safety,
            "cultural_activities": cultural_activities,
            "green_preference": green_preference
        }
    except ValueError:
        print("Ошибка ввода. Пожалуйста, введите корректные значения.")
        return get_user_preferences()

def calculate_similarity(city, user_prefs):
    """Расчет схожести города с предпочтениями пользователя."""
    weights = {
        "climate": 5,  
        "weather_stability": 2,
        "population": 5,  
        "city_rhythm": 2,
        "infrastructure": 1,
        "greenery": 1,
        "work_mode": 1,
        "lifestyle": 1,
        "preferred_objects": 1,
        "safety": 2,
        "cultural_activities": 1,
        "green_preference": 1,
    }
    
    score = 0

    # Ключевые параметры: климат и население с большим весом
    score += weights["climate"] * abs(user_prefs["climate"] - city["climate"])
    score += weights["population"] * abs(user_prefs["population"] - city["population"])
    
    # Другие параметры
    score += weights["weather_stability"] * abs(user_prefs["weather_stability"] - city["weather_stability"])
    score += weights["city_rhythm"] * abs(user_prefs["city_rhythm"] - city["city_rhythm"])
    score += weights["infrastructure"] * abs(user_prefs["infrastructure"] - city["infrastructure"])
    score += weights["greenery"] * abs(user_prefs["greenery"] - city["greenery"])
    score += weights["safety"] * abs(user_prefs["safety"] - city["safety"])
    score += weights["cultural_activities"] * abs(user_prefs["cultural_activities"] - city["cultural_activities"])
    score += weights["green_preference"] * abs(user_prefs["green_preference"] - city["green_preference"])

    # Work mode, lifestyle and preferred objects
    score += weights["work_mode"] * (1 - len(set(user_prefs["work_mode"]) & set(city["work_mode"])) / len(user_prefs["work_mode"]))
    score += weights["lifestyle"] * (1 - len(set(user_prefs["lifestyle"]) & set(city["lifestyle"])) / len(user_prefs["lifestyle"]))
    score += weights["preferred_objects"] * (1 - len(set(user_prefs["preferred_objects"]) & set(city["preferred_objects"])) / len(user_prefs["preferred_objects"]))

    return score

def find_best_cities(user_prefs, cities, top_n=5):
    """Найти наиболее подходящие города с сортировкой по убыванию соответствия."""
    city_scores = [(city, calculate_similarity(city, user_prefs)) for city in cities]
    
    # Сортировка по возрастанию score (меньше = лучше)
    city_scores.sort(key=lambda x: x[1])  # Сортировка по минимальному значению схожести
    
    # Возвращаем top_n лучших городов
    return [city for city, _ in city_scores[:top_n]]

# Главная программа
if __name__ == "__main__":
    # Загрузка данных из JSON файла
    cities = load_cities_from_json('cities.json')

    # Получение предпочтений пользователя
    user_preferences = get_user_preferences()

    # Рекомендация лучших городов
    recommended_cities = find_best_cities(user_preferences, cities, top_n=5)

    # Вывод результата
    if recommended_cities:
        print("Наиболее подходящие города (в порядке убывания соответствия):")
        for city in recommended_cities:
            print(f"- {city['name']}")
    else:
        print("К сожалению, подходящих городов не найдено.")
