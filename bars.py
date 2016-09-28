import json
import math


def load_data(filepath):
    """
        @param filepath Путь к файлу в формате json
        @return Данные файла
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print('File not found: "{}"'.format(filepath))
    except PermissionError:
        print('Access to file denied: "{}"'.format(filepath))
    except Exception as e:
        print('Error: {}'.format(e))

def get_content(bar):
    """
        @param bar Данные бара
        @return Контент
    """
    content = bar['Cells']['Name'] + '\n'
    content += 'Количество мест: %s \n' % bar['Cells']['SeatsCount']
    content += '{}, {}, {} \n'.format(
        bar['Cells']['AdmArea'],
        bar['Cells']['District'],
        bar['Cells']['Address'])
    content += 'Контакты:\n'
    for phone in bar['Cells']['PublicPhone']:
        content += '  - ' + phone['PublicPhone'] + '\n'
    content += '\n'
    return content

def get_bar(data, type_bar=None):
    """
        @param data Список дынных
        @param type_bar Тип искомого бара
        @return Самый большой или маленький бар из списка
    """
    if type_bar not in ['biggest', 'smallest']:
        print('Не указан тип бара!')
        return None
    seeking_bar = data.pop(0)
    for bar in data:
        if type_bar is 'biggest':
            if bar['Cells']['SeatsCount'] > seeking_bar['Cells']['SeatsCount']:
                seeking_bar = bar
        if type_bar is 'smallest':
            if bar['Cells']['SeatsCount'] < seeking_bar['Cells']['SeatsCount']:
                seeking_bar = bar
    return get_content(seeking_bar)

def get_gps_coordinates():
    """
        @return gps-координаты
    """
    while True:
        try:
            print('Введите текущие gps-координаты (долгота, широта) через запятую:')
            longitude, latitude = map(float, input('> ').split(','))
            break
        except Exception as e:
            print('Ошибка: не верно введены gps-координаты! Введите число. (Пример: "55.12345, 37.12345")')
    return longitude, latitude


def get_distance(bar, longitude, latitude):
    """
        @param bar Список дынных
        @param longitude Долгота
        @param latitude Широта
        @return дистанция по gps-координатам
    """
    longitude_bar = bar['Cells']['geoData']['coordinates'][1]
    latitude_bar = bar['Cells']['geoData']['coordinates'][0]
    return abs(math.sqrt((longitude - longitude_bar)**2 + (latitude - latitude_bar)**2))

def get_closest_bar(data, longitude, latitude, show_count=1):
    """
        @param data Список дынных
        @param longitude Долгота
        @param latitude Широта
        @return Контен
    """
    for index, bar in enumerate(data):
        # Расчёт растояния до ближайшей geo-точки
        distance = get_distance(bar, longitude, latitude)
        data[index]['Distance'] = round(distance, 15)
    # Отсортируем список
    data.sort(key=lambda x: x['Distance'])
    content = ''
    for bar in data[:show_count]:
        content += get_content(bar)
    return content

def main():
    print('Введите путь к файлу со список московских баров (в формате json):')
    data = load_data(input('> '))
    if data:
        # Получение gps-координаты с клавиатуры
        longitude, latitude = get_gps_coordinates()
        print('-'*100)
        print('Cамый большой бар:\n', get_bar(data, type_bar='biggest'))
        print('-'*100)
        print('Cамый маленький бар:\n', get_bar(data, type_bar='smallest'))
        print('-'*100)
        print('Cамые ближайшие бары:\n', get_closest_bar(data, longitude, latitude, 1))

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Принудительное завершение')
    finally:
        pass


