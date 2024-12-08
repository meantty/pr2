from flask import Flask, request, render_template
from web.basic_requests import check_weather_by_location_key, get_location_key_by_name, get_location_key_by_coordinates

# Создаем экземпляр Flask-приложения
app = Flask(__name__)

@app.route('/')
def form():
    """
    Отображает форму для ввода данных о местоположении.

    :return: HTML-страница с формой для ввода адресов.
    """
    return render_template('form.html')  # Возвращаем шаблон формы

@app.route('/check-weather', methods=['POST'])
def check_weather():
    """
    Обрабатывает запрос на проверку погоды по введенным адресам.

    :return: HTML-страница с результатами проверки погоды или сообщение об ошибке.
    """
    try:
        # Получаем данные из формы о начальной точке
        start_address = request.form.get('start_address')  # Адрес начала маршрута
        if start_address:
            # Если адрес указан, получаем ключ локации по имени
            start_lk = get_location_key_by_name(start_address)
        else:
            # Если адрес не указан, пытаемся получить координаты
            start_latitude = request.form.get('start_latitude')
            start_longitude = request.form.get('start_longitude')
            start_lk = get_location_key_by_coordinates(start_latitude, start_longitude)

        # Получаем данные из формы о конечной точке
        end_address = request.form.get('end_address')  # Адрес конца маршрута
        if end_address:
            # Если адрес указан, получаем ключ локации по имени
            end_lk = get_location_key_by_name(end_address)
        else:
            # Если адрес не указан, пытаемся получить координаты
            end_latitude = request.form.get('end_latitude')
            end_longitude = request.form.get('end_longitude')
            end_lk = get_location_key_by_coordinates(end_latitude, end_longitude)

        # Проверяем, удалось ли получить ключи локаций
        if not end_lk or not start_lk:
            raise ValueError("Ошибка: недостаточно данных для определения координат начала или конца маршрута.")

        # Проверяем погоду на начальной и конечной точках
        start_weather = check_weather_by_location_key(start_lk)
        end_weather = check_weather_by_location_key(end_lk)

        # Отображаем результаты на странице
        return render_template('result.html', start_weather=start_weather, end_weather=end_weather, error=None)

    except ValueError as e:
        # Безопасное сообщение об ошибке для пользователя
        error_message = str(e)
        return render_template('result.html', error=error_message)

    except Exception as e:
        # Общая обработка ошибок с безопасным сообщением
        print(f"Неожиданная ошибка: {e}")
        error_message = "Произошла ошибка при обработке запроса. Пожалуйста, попробуйте снова."
        return render_template('result.html', error=error_message)

if __name__ == '__main__':
    app.run()

