import json
from math import sqrt


def load_data(filepath):
    """
        @param filepath Путь к файлу в формате json
        @return Данные файла json
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_bar_seats_info(bar):
    return bar['Cells']['SeatsCount']

def get_bar_distance(bar, usr_longitude, usr_latitude):
    index_bar_longitude = 0
    index_bar_latitude = 1
    bar_longitude = bar['Cells']['geoData']['coordinates'][index_bar_longitude]
    bar_latitude = bar['Cells']['geoData']['coordinates'][index_bar_latitude]
    return sqrt(pow((bar_longitude - usr_longitude), 2) + pow((bar_latitude - usr_latitude), 2))

def get_biggest_bar(list_of_bars):
    """
        @param list_of_bars Список дынных баров
        @return Данные бара, самый большой бар из списка
    """
    return max(list_of_bars, key=get_bar_seats_info)

def get_smallest_bar(list_of_bars):
    """
        @param list_of_bars Список дынных баров
        @return Данные бара, самый маленький бар из списка
    """
    return min(list_of_bars, key=get_bar_seats_info)

def get_closest_bar(list_of_bars, usr_longitude, usr_latitude):
    """
        @param list_of_bars Список дынных
        @param usr_longitude Долгота
        @param usr_latitude Широта
        @return Ближайший бар
    """
    return min(list_of_bars, key=lambda bar: get_bar_distance(bar, usr_longitude, usr_latitude))

def get_list_of_bars():
    print('Введите путь к файлу московских баров (в формате json): ')
    while True:
        try:
            path_to_file = input('> ')
            list_of_bars = load_data(path_to_file)
            break
        except IOError:
            print('Введите корректный путь до файла.')

    return list_of_bars

def def_gps_coordinates():
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
    return longitude, latitude

def display_results_on_screen(biggest_bar, smallest_bar, closest_bar):
    
    print('\n# Самый вместительный бар: \n> {}. {};'.format(
        biggest_bar['Cells']['Name'],
        biggest_bar['Cells']['Address']))
    
    print('\n# Самый маленький бар: \n> {}. {};'.format(
        smallest_bar['Cells']['Name'],
        smallest_bar['Cells']['Address']))

    print('\n# Ближайший бар: \n> {}. {};'.format(
        closest_bar['Cells']['Name'],
        closest_bar['Cells']['Address']))



if __name__ == '__main__':
    try:
        list_of_bars = get_list_of_bars()
        longitude, latitude = def_gps_coordinates()
        display_results_on_screen(
            get_biggest_bar(list_of_bars),
            get_smallest_bar(list_of_bars),
            get_closest_bar(list_of_bars, longitude, latitude))
    except KeyboardInterrupt:
        print('Принудительное завершение')
    finally:
        pass

