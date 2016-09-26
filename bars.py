import json
import math


def load_data(filepath):
    f = open(filepath, 'r')
    content = f.read()
    f.close()
    return json.loads(content)

def get_biggest_bar(data):
    """
        @param data Список дынных
        @return Самый большой бар из списка
    """
    biggest = None
    for bar in data:
        if biggest is None:
            biggest = bar
            continue
        if bar['Cells']['SeatsCount'] > biggest['Cells']['SeatsCount']:
            biggest = bar
    return biggest

def get_smallest_bar(data):
    """
        @param data Список дынных
        @return Самый маленький бар из списка
    """
    smallest = None
    for bar in data:
        if smallest is None:
            smallest = bar
            continue
        if bar['Cells']['SeatsCount'] < smallest['Cells']['SeatsCount']:
            smallest = bar
    return smallest


def get_closest_bar(data, longitude, latitude):
    """
        @param data Список дынных
        @param longitude Долгота
        @param latitude Широта
    """
    for index, bar in enumerate(data):
        # Долгота бара
        x = bar['Cells']['geoData']['coordinates'][1]
        # Широта бара
        y = bar['Cells']['geoData']['coordinates'][0]
        # Расчёт растояния до ближайшей geo-точки
        distance = abs(math.sqrt((longitude - x)**2 + (latitude - y)**2))
        data[index]['Distance'] = round(distance, 15)
    # Отсортируем список
    data.sort(key=lambda x: x['Distance'])
    return data

def main():
    content = ''

    # Получим данные
    data = load_data('bars.json')

    # Самый большой бар
    count_biggest_bar = get_biggest_bar(data)
    content += 'Самый большой бар:\n'
    content += count_biggest_bar['Cells']['Name'] + '\n'
    content += 'Количество мест: %s \n' % count_biggest_bar['Cells']['SeatsCount']
    content += '{}, {}, {} \n'.format(
        count_biggest_bar['Cells']['AdmArea'],
        count_biggest_bar['Cells']['District'],
        count_biggest_bar['Cells']['Address'])
    content += 'Контакты:\n'
    for phone in count_biggest_bar['Cells']['PublicPhone']:
        content += '  - ' + phone['PublicPhone'] + '\n'
    content += '\n'

    # Самый маленький бар
    count_smallest_bar = get_smallest_bar(data)
    content += 'Самый маленький бар:\n'
    content += count_smallest_bar['Cells']['Name'] + '\n'
    content += 'Количество мест: %s \n' % count_smallest_bar['Cells']['SeatsCount']
    content += '{}, {}, {} \n'.format(
        count_smallest_bar['Cells']['AdmArea'],
        count_smallest_bar['Cells']['District'],
        count_smallest_bar['Cells']['Address'])
    content += 'Контакты:\n'
    for phone in count_smallest_bar['Cells']['PublicPhone']:
        content += '  - ' + phone['PublicPhone'] + '\n'
    content += '\n'

    # Проинфирмируем
    print(content)


    # Ближайший бар по координатам
    content = ''

    # Вод данных с клавиатуры
    while True:
        try:
            longitude = float(input('Введите долготу: '))
            break
        except Exception as e:
            print('Ошибка: не верно введена долгота! Введите число. (Пример: 55.750623563675717)')
    while True:
        try:
            latitude = float(input('Введите широту: '))
            break
        except Exception as e:
            print('Ошибка: не верно введена широта! Введите число. (Пример: 37.582406638647662)')


    # Расчёт
    closest_bars = get_closest_bar(data, longitude, latitude)

    # Количество ближайших баров
    show_closest_bars = 1

    # Контент
    for index, bar in enumerate(closest_bars):
        content += bar['Cells']['Name'] + '\n'
        content += 'Количество мест: %s \n' % bar['Cells']['SeatsCount']
        content += '{}, {}, {} \n'.format(
            bar['Cells']['AdmArea'],
            bar['Cells']['District'],
            bar['Cells']['Address'])
        content += 'Контакты:\n'
        for phone in bar['Cells']['PublicPhone']:
            content += '  - ' + phone['PublicPhone'] + '\n'
        content += '\n'
        if index + 1 == show_closest_bars:
            break

    # Проинфирмируем
    print(content)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Принудительное завершение')
    finally:
        pass


