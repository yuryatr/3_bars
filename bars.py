import sys
import json
from math import sqrt


def load_data(filepath):
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
    return max(list_of_bars, key=get_bar_seats_info)

def get_smallest_bar(list_of_bars):
    return min(list_of_bars, key=get_bar_seats_info)

def get_closest_bar(list_of_bars, usr_longitude, usr_latitude):
    return min(list_of_bars, key=lambda bar: get_bar_distance(bar, usr_longitude, usr_latitude))

def get_input_list_of_bars():
    try:
        path_to_file = input('> ')
        list_of_bars = load_data(path_to_file)
    except IOError:
        return
    else:
        return list_of_bars

def gef_input_gps_coordinates():
    try:
        gps_coordinates = input('> ')
        longitude, latitude = map(float, gps_coordinates.split(','))
    except ValueError as e:
        return
    else:
        return {'lon': longitude, 'lat': latitude}

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
        print('Введите путь к файлу московских баров (в формате json): ')
        list_of_bars = get_input_list_of_bars()
        if list_of_bars is None:
            print('Введите корректный путь до файла.')
            sys.exit(1)

        print('Введите gps-координаты (долгота, широта) через запятую '
              '(Пример: "х.ххххххххххххххх, х.ххххххххххххххх"):')
        coordinates = gef_input_gps_coordinates()
        if coordinates is None:
            print('Ошибка: не верно введены gps-координаты! '
                  'Введите число. Пример: "х.ххххххххххххххх, х.ххххххххххххххх"')
            sys.exit(1)

        display_results_on_screen(
            get_biggest_bar(list_of_bars),
            get_smallest_bar(list_of_bars),
            get_closest_bar(list_of_bars, coordinates['lon'], coordinates['lat']))
    except KeyboardInterrupt:
        print('Принудительное завершение')
    finally:
        sys.exit(0)

