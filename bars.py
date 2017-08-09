import json
import math


def load_data(filepath):
    """
        @param filepath Путь к файлу в формате json
        @return Данные файла json
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_biggest_bar(list_of_bars):
    """
        @param list_of_bars Список дынных баров
        @return Данные, самый большой бар из списка
    """
    seeking_bar = list_of_bars.pop(0)
    for bar in list_of_bars:
        if bar['Cells']['SeatsCount'] > seeking_bar['Cells']['SeatsCount']:
            seeking_bar = bar
    return seeking_bar

def get_smallest_bar(list_of_bars):
    """
        @param list_of_bars Список дынных баров
        @return Данные, самый маленький бар из списка
    """
    seeking_bar = list_of_bars.pop(0)
    for bar in list_of_bars:
        if bar['Cells']['SeatsCount'] < seeking_bar['Cells']['SeatsCount']:
            seeking_bar = bar
    return seeking_bar

def get_closest_bar(list_of_bars, longitude, latitude, number_of_returned_bars=1):
    """
        @param list_of_bars Список дынных
        @param longitude Долгота
        @param latitude Широта
        @param number_of_returned_bars Количество возвращаемых ближайших баров
        @return Список ближайших баров
    """
    if not list_of_bars:
        return []

    for index, bar in enumerate(list_of_bars):
        longitude_bar = bar['Cells']['geoData']['coordinates'][0]
        latitude_bar = bar['Cells']['geoData']['coordinates'][1]
        distance = abs(math.sqrt((longitude - longitude_bar)**2 + (latitude - latitude_bar)**2))
        list_of_bars[index]['Distance'] = round(distance, 15)

    list_of_bars.sort(key=lambda x: x['Distance'])

    if number_of_returned_bars >= len(list_of_bars):
        return list_of_bars

    return list_of_bars[:number_of_returned_bars]

def get_data_from_the_user():

    print('Введите путь к файлу московских баров (в формате json): ')
    while True:
        try:
            path_to_file = input('> ')
            list_of_bars = load_data(path_to_file)
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

    return list_of_bars, longitude, latitude

def display_results_on_screen(biggest_bar, smallest_bar, closest_bars):
    
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



if __name__ == '__main__':
    try:
        list_of_bars, longitude, latitude = get_data_from_the_user()

        biggest_bar = get_biggest_bar(list_of_bars)
        smallest_bar = get_smallest_bar(list_of_bars)
        closest_bars = get_closest_bar(list_of_bars, longitude, latitude, number_of_returned_bars=3)

        display_results_on_screen(biggest_bar, smallest_bar, closest_bars)

    except KeyboardInterrupt:
        print('Принудительное завершение')
    finally:
        pass

