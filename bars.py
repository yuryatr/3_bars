import json
import math


def load_data(filepath):
    """
        @param filepath Путь к файлу в формате json
        @return Данные файла json
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_biggest_bar(data):
    """
        @param data Список дынных баров
        @return Данные, самый большой бар из списка
    """
    seeking_bar = data.pop(0)
    for bar in data:
        if bar['Cells']['SeatsCount'] > seeking_bar['Cells']['SeatsCount']:
            seeking_bar = bar
    return seeking_bar

def get_smallest_bar(data):
    """
        @param data Список дынных баров
        @return Данные, самый маленький бар из списка
    """
    seeking_bar = data.pop(0)
    for bar in data:
        if bar['Cells']['SeatsCount'] < seeking_bar['Cells']['SeatsCount']:
            seeking_bar = bar
    return seeking_bar

def get_closest_bar(data, longitude, latitude, show_count=1):
    """
        @param data Список дынных
        @param longitude Долгота
        @param latitude Широта
        @show_count Количество возвращаемых ближайших баров
        @return Список ближайших баров
    """
    # Нет смысла продолжать
    if not data:
        return []

    for index, bar in enumerate(data):
        # Пулучиь значения координат бара
        longitude_bar = bar['Cells']['geoData']['coordinates'][0]
        latitude_bar = bar['Cells']['geoData']['coordinates'][1]
        
        # Расчёт растояния до ближайшей geo-точки
        distance = abs(math.sqrt((longitude - longitude_bar)**2 + (latitude - latitude_bar)**2))
        data[index]['Distance'] = round(distance, 15)

    # Отсортируем список
    data.sort(key=lambda x: x['Distance'])

    # Если указано больше
    if show_count >= len(data):
        return data

    # Вернуть срез данных
    return data[:show_count]


if __name__ == '__main__':
    try:

        # *******************************************
        # Полученных данных
        # *******************************************

        print('Введите путь к файлу московских баров (в формате json): ')
        while True:
            try:
                path_to_file = input('> ')
                data_bars = load_data(path_to_file)
                break
            except IOError:
                print('Введите корректный путь до файла.')

        print('Введите gps-координаты (долгота, широта) через запятую '
              '(Пример: "х.ххххххххххххххх, х.ххххххххххххххх"):')

        while True:
            try:
                gps_coordinates = input('> ')
                longitude, latitude = map(float, gps_coordinates.split(','))
                break
            except ValueError as e:
                print('Ошибка: не верно введены gps-координаты! '
                      'Введите число. Пример: "х.ххххххххххххххх, х.ххххххххххххххх"')

        # *******************************************
        # Обработка полученных данных
        # *******************************************

        # Получить самый большой бар
        biggest_bar = get_biggest_bar(data_bars)
        
        # Получить самый маленький бар
        smallest_bar = get_smallest_bar(data_bars)

        # Получить 3 ближайших баров (список)
        closest_bars = get_closest_bar(data_bars, longitude, latitude, 3)

        
        # *******************************************
        # Вывод результатов обработки
        # *******************************************

        print('\n# Самый вместительный бар: \n> {}. {};'.format(
            biggest_bar['Cells']['Name'],
            biggest_bar['Cells']['Address']))
        
        print('\n# Самый маленький бар: \n> {}. {};'.format(
            smallest_bar['Cells']['Name'],
            smallest_bar['Cells']['Address']))

        print('\n# Ближайшие {} бара:'.format(len(closest_bars)))
        for i, closest_bar in enumerate(closest_bars):
            print('> {}) {}. {};'.format(i+1,
                closest_bar['Cells']['Name'],
                closest_bar['Cells']['Address']))

    except KeyboardInterrupt:
        print('Принудительное завершение')
    finally:
        pass

