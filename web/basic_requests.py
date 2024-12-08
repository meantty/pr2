import requests
from dotenv import load_dotenv
import os

# Загружаем переменные окружения для доступа к API
load_dotenv()
API_KEY = os.getenv('WEATHER_API_KEY')

if not API_KEY:
    raise ValueError("API ключ не установлен. Пожалуйста, проверьте ваш .env файл.")

def get_location_key_by_coordinates(latitude, longitude):
    try:
        url = f"http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey={API_KEY}&q={latitude},{longitude}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['Key']
    except Exception as e:
        print(f"Ошибка при получении ключа локации по координатам: {e}")
        return None

def get_location_key_by_name(address):
    try:
        url = f"http://dataservice.accuweather.com/locations/v1/cities/autocomplete?apikey={API_KEY}&q={address}&language=ru"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data[0]['Key'] if data else None
    except Exception as e:
        print(f"Ошибка при получении ключа локации для адреса {address}: {e}")
        return None

def get_current_temperature_by_location_key(location_key):
    try:
        url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={API_KEY}&language=ru&details=True"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data[0]['Temperature']['Metric']['Value'], data[0]['WeatherText'] if data else (None, None)
    except Exception as e:
        raise RuntimeError(f"Ошибка при получении текущей температуры: {e}")

def get_current_conditions_by_location_key(location_key):
    try:
        url = f"http://dataservice.accuweather.com/forecasts/v1/daily/1day/{location_key}?apikey={API_KEY}&language=ru&details=true"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if 'DailyForecasts' in data and data['DailyForecasts']:
            min_temperature = round(5/9 * (data['DailyForecasts'][0]['Temperature']['Minimum']['Value'] - 32), 2)
            max_temperature = round(5/9 * (data['DailyForecasts'][0]['Temperature']['Maximum']['Value'] - 32), 2)
            wind_speed = round(data['DailyForecasts'][0]['Day']['Wind']['Speed']['Value'] * 1.61, 2)
            precipitation_probability = data['DailyForecasts'][0]['Day']['PrecipitationProbability']
            return min_temperature, max_temperature, wind_speed, precipitation_probability
        else:
            return None
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Ошибка сети: {e}")
    except (KeyError, IndexError) as e:
        raise RuntimeError(f"Ошибка доступа к данным: {e}")

def check_weather_by_location_key(lk):
    if lk is None:
        raise ValueError("Невозможно получить данные для указанного местоположения. Пожалуйста, проверьте введенные данные.")

    try:
        current_temperature_result = get_current_temperature_by_location_key(lk)
        if current_temperature_result is None:
            raise ValueError("Не удалось получить текущую температуру.")

        current_conditions_result = get_current_conditions_by_location_key(lk)
        if current_conditions_result is None:
            raise ValueError("Не удалось получить текущие погодные условия.")

        min_temperature, max_temperature, wind_speed, precipitation_probability = current_conditions_result

        data = {
            "min_temperature": min_temperature,
            "max_temperature": max_temperature,
            "wind_speed": wind_speed,
            "precipitation_probability": precipitation_probability,
            "temperature_summary": None,
            "wind_summary": None,
            "precipitation_summary": None,
            "weather_summary": 'Погода неблагоприятная',
        }

        if min_temperature < 0 or max_temperature > 35:
            data['temperature_summary'] = "Температура неблагоприятная"
        elif wind_speed > 50:
            data['wind_summary'] = "Сильный ветер"
        elif precipitation_probability > 70:
            data['precipitation_summary'] = "Высокая вероятность осадков"
        else:
            data['weather_summary'] = "Погода благоприятная"

        return data

    except Exception as e:
        print(f"Ошибка при получении данных о погоде: {e}")
        raise

def main():
    start_address = 'Москва'
    end_address = 'Санкт-Петербург'

    start_lk = get_location_key_by_name(start_address)
    end_lk = get_location_key_by_name(end_address)

    start_weather = check_weather_by_location_key(start_lk)
    end_weather = check_weather_by_location_key(end_lk)

    print(start_weather)
    print(end_weather)

if __name__ == '__main__':
    main()