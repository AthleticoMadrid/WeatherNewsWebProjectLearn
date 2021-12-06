from flask import current_app       #позволяет обращаться к текущему flask-приложению
import requests         #посылает запрос к серверу и возвращает результат

def weather_by_city(city_name):     #функция погоды сейчас (принимает название города)
    weather_url = current_app.config['WEATHER_URL']   #наш url из config.py
    params = {      #их можно взять из url (всё что после ?)
        "key": current_app.config['WEATHER_API_KEY'],       # наш API из config.py
        "q": city_name,     #функция будет запрашивать погоду не только для Оренбурга
        "format": "json",
        "num_of_days": 1,
        "lang": "ru",
    }
    try:
        result = requests.get(weather_url, params=params)  #идём на сервер
        result.raise_for_status()   #сгенерирует исключение если сервер ответит кодом начинающимся с 4хх или 5хх
        weather = result.json()     #получаем результат (словарь со списками json)
        if 'data' in weather:       #если ключ 'data' есть в полученном словаре
            if 'current_condition' in weather['data']:  #а ключ 'current_condition' есть в секции 'data'
                try:
                    return weather['data']['current_condition'][0]  #возвращаем 0 элемент списка 'current_condition'
                except(IndexError, TypeError):
                    return False
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка. Возможно отсутствует подключение к сети')
        return False
    return False

if __name__ == '__main__':
    w = weather_by_city("Orsk,Russia")
    print(w)
