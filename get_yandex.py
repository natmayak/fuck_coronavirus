import requests
import settings

API_URL = 'https://search-maps.yandex.ru/v1/'

PARAMS = dict(text='аптека', ll="37.575637, 55.742933", spn="0.01000,0.01000", lang='ru_RU', apikey=settings.API_KEY_YNDX)


response = requests.get(API_URL, params=PARAMS)
print(response)

results = response.json()
print(results)
#pharmacies = results['features']
# index_number = 0
# for pharmacy in pharmacies:
#     address = pharmacies[index_number]['properties']['description']
#     index_number += 1
#     print(address)

places = results['features']
lst_of_places = list()
lst_of_names = list()
lst_of_links = list()
index_number = 0
while index_number <= 2:
    lst_of_places.append(places[index_number]['geometry']['coordinates'])
    lst_of_names.append(places[index_number]['properties']['name'])
    #link = f'https://yandex.ru/maps/?text={lst_of_places[index_number][0]}%2C{lst_of_places[index_number][1]}'
    lst_of_links.append(f'https://yandex.ru/maps/?text={lst_of_places[index_number][1]}%2C{lst_of_places[index_number][2]}')
    index_number += 1
print(lst_of_places)
print(lst_of_names)
print(lst_of_links)

# todo надо забирать первые три аптеки и сформировать 3 ссылки

# for index, pharmacy in pharmacies.items():
#     address = pharmacy['properties']['description']

# {'longitude': 37.575637, 'latitude': 55.742933}
#               37.575933,             55.739966
#               37.563105,             55.74053393
# {'longitude': 37.528929, 'latitude': 55.775318}

# {'type': 'FeatureCollection', 'properties': {'ResponseMetaData': {'SearchResponse': {'found': 91, 'display': 'multiple', 'boundedBy': [[37.55707582, 55.73117794], [37.59693218, 55.75361368]]}, 'SearchRequest': {'request': 'аптеки', 'skip': 0, 'results': 10, 'boundedBy': [[37.048427, 55.43644866], [38.175903, 56.04690174]]}}},
# 'features':
# [{'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [37.583526, 55.748655]},'properties': {'name': 'Здоров.ру', 'description': 'Смоленская площадь, 6, Москва, Россия', 'boundedBy': [[37.5794205, 55.74633943], [37.5876315, 55.75097043]], 'CompanyMetaData': {'id': '200381815542', 'name': 'Здоров.ру', 'address': 'Россия, Москва, Смоленская площадь, 6', 'url': 'https://zdorov.ru/', 'Phones': [{'type': 'phone', 'formatted': '+7 (495) 363-35-00'}], 'Categories': [{'class': 'drugstores', 'name': 'Аптека'}], 'Hours': {'text': 'ежедневно, 7:00–23:00', 'Availabilities': [{'Intervals': [{'from': '07:00:00', 'to': '23:00:00'}], 'Everyday': True}]}}}},
# {'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [37.563686, 55.737691]},'properties': {'name': 'Аптека', 'description': 'Бережковская наб., 12, Москва, Россия', 'boundedBy': [[37.5626615, 55.737113], [37.5647105, 55.738269]], 'CompanyMetaData': {'id': '154436329324', 'name': 'Аптека', 'address': 'Россия, Москва, Бережковская набережная, 12', 'Categories': [{'class': 'drugstores', 'name': 'Аптека'}], 'Hours': {'text': 'пн-пт 9:00–21:00; сб,вс 10:00–20:00', 'Availabilities': [{'Intervals': [{'from': '09:00:00', 'to': '21:00:00'}], 'Monday': True, 'Tuesday': True, 'Wednesday': True, 'Thursday': True, 'Friday': True}, {'Intervals': [{'from': '10:00:00', 'to': '20:00:00'}], 'Saturday': True, 'Sunday': True}]}}}},
# {'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [37.574325, 55.739863]},'properties': {'name': 'Ригла', 'description': '1-й Вражский пер., 4, Москва, Россия', 'boundedBy': [[37.57022, 55.73754693], [37.57843, 55.74217893]], 'CompanyMetaData': {'id': '128120971028', 'name': 'Ригла', 'address': 'Россия, Москва, 1-й Вражский переулок, 4', 'url': 'http://www.rigla.ru/', 'Phones': [{'type': 'phone', 'formatted': '8 (800) 777-03-03'}, {'type': 'phone', 'formatted': '+7 (495) 730-27-30'}], 'Categories': [{'class': 'drugstores', 'name': 'Аптека'}]}}},
# {'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [37.58932, 55.746785]},'properties': {'name': 'Аптека', 'description': 'пер. Сивцев Вражек, 35, Москва, Россия', 'boundedBy': [[37.5852145, 55.74446943], [37.5934255, 55.74910043]], 'CompanyMetaData': {'id': '1025414359', 'name': 'Аптека', 'address': 'Россия, Москва, переулок Сивцев Вражек, 35', 'url': 'https://vipmed.ru/otdelenie/apteka', 'Phones': [{'type': 'phone', 'formatted': '+7 (499) 241-25-25'}], 'Categories': [{'class': 'drugstores', 'name': 'Аптека'}, {'class': 'malls', 'name': 'Салон оптики'}], 'Hours': {'text': 'пн-пт 8:00–20:00; сб 8:00–15:00', 'Availabilities': [{'Intervals': [{'from': '08:00:00', 'to': '20:00:00'}], 'Monday': True, 'Tuesday': True, 'Wednesday': True, 'Thursday': True, 'Friday': True}, {'Intervals': [{'from': '08:00:00', 'to': '15:00:00'}], 'Saturday': True}]}}}},
# {'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [37.575933, 55.739966]},'properties': {'name': 'Аптека столицы', 'description': 'ул. Плющиха, 42, Москва, Россия', 'boundedBy': [[37.5718275, 55.73764993], [37.5800385, 55.74228193]], 'CompanyMetaData': {'id': '1245534473', 'name': 'Аптека столицы', 'address': 'Россия, Москва, улица Плющиха, 42', 'url': 'http://www.cloikk.ru/', 'Phones': [{'type': 'phone', 'formatted': '+7 (495) 974-73-19'}, {'type': 'phone', 'formatted': '+7 (499) 255-85-87'}, {'type': 'phone', 'formatted': '+7 (499) 245-76-96'}, {'type': 'phone', 'formatted': '+7 (499) 255-82-31'}, {'type': 'phone', 'formatted': '+7 (495) 974-79-22'}], 'Categories': [{'class': 'drugstores', 'name': 'Аптека'}], 'Hours': {'text': 'пн-пт 8:00–21:00; сб 9:00–20:00; вс 10:00–18:00', 'Availabilities': [{'Intervals': [{'from': '08:00:00', 'to': '21:00:00'}], 'Monday': True, 'Tuesday': True, 'Wednesday': True, 'Thursday': True, 'Friday': True}, {'Intervals': [{'from': '09:00:00', 'to': '20:00:00'}], 'Saturday': True}, {'Intervals': [{'from': '10:00:00', 'to': '18:00:00'}], 'Sunday': True}]}}}}, {'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [37.583796, 55.748387]},
# 'properties': {'name': 'Эвалар', 'description': 'Карманицкий пер., 9, Москва, Россия', 'boundedBy': [[37.5796905, 55.74607143], [37.5879015, 55.75070243]], 'CompanyMetaData': {'id': '237214141508', 'name': 'Эвалар', 'address': 'Россия, Москва, Карманицкий переулок, 9', 'url': 'https://www.evalar.ru/', 'Phones': [{'type': 'phone', 'formatted': '8 (800) 200-52-52'}, {'type': 'phone', 'formatted': '+7 (499) 241-87-88'}], 'Categories': [{'class': 'drugstores', 'name': 'Аптека'}], 'Hours': {'text': 'пн-пт 8:00–22:00; сб,вс 10:00–21:00', 'Availabilities': [{'Intervals': [{'from': '08:00:00', 'to': '22:00:00'}], 'Monday': True, 'Tuesday': True, 'Wednesday': True, 'Thursday': True, 'Friday': True}, {'Intervals': [{'from': '10:00:00', 'to': '21:00:00'}], 'Saturday': True, 'Sunday': True}]}}}}, {'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [37.58461, 55.739909]},
# 'properties': {'name': 'Аптека столицы', 'description': 'Смоленский бул., 3-5с1Б, Москва, Россия', 'boundedBy': [[37.5805045, 55.73759293], [37.5887155, 55.74222493]], 'CompanyMetaData': {'id': '1142205299', 'name': 'Аптека столицы', 'address': 'Россия, Москва, Смоленский бульвар, 3-5с1Б', 'url': 'http://www.cloikk.ru/', 'Phones': [{'type': 'phone', 'formatted': '+7 (499) 246-58-40'}, {'type': 'phone', 'formatted': '+7 (495) 974-73-19'}, {'type': 'phone', 'formatted': '+7 (499) 246-12-48'}, {'type': 'phone', 'formatted': '+7 (495) 974-79-22'}], 'Categories': [{'class': 'drugstores', 'name': 'Аптека'}], 'Hours': {'text': 'пн-пт 8:00–21:00; сб 9:00–20:00; вс 10:00–18:00', 'Availabilities': [{'Intervals': [{'from': '08:00:00', 'to': '21:00:00'}], 'Monday': True, 'Tuesday': True, 'Wednesday': True, 'Thursday': True, 'Friday': True}, {'Intervals': [{'from': '09:00:00', 'to': '20:00:00'}], 'Saturday': True}, {'Intervals': [{'from': '10:00:00', 'to': '18:00:00'}], 'Sunday': True}]}}}}, {'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [37.586967, 55.747926]},
# 'properties': {'name': 'Самсон-Фарма', 'description': 'ул. Арбат, 51, стр. 1, Москва, Россия', 'boundedBy': [[37.5828615, 55.74561043], [37.5910725, 55.75024143]], 'CompanyMetaData': {'id': '23043314667', 'name': 'Самсон-Фарма', 'address': 'Россия, Москва, улица Арбат, 51, стр. 1', 'url': 'https://samson-pharma.ru/', 'Phones': [{'type': 'phone', 'formatted': '+7 (495) 587-77-77'}], 'Categories': [{'class': 'drugstores', 'name': 'Аптека'}], 'Hours': {'text': 'ежедневно, 9:00–21:00', 'Availabilities': [{'Intervals': [{'from': '09:00:00', 'to': '21:00:00'}], 'Everyday': True}]}}}}, {'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [37.56721, 55.74285]},
# 'properties': {'name': 'Неофарм', 'description': 'площадь Киевского Вокзала, 1, Москва, Россия', 'boundedBy': [[37.563105, 55.74053393], [37.571315, 55.74516593]], 'CompanyMetaData': {'id': '52040331148', 'name': 'Неофарм', 'address': 'Россия, Москва, площадь Киевского Вокзала, 1', 'url': 'http://neopharm.ru/', 'Phones': [{'type': 'phone', 'formatted': '+7 (495) 585-55-15'}], 'Categories': [{'class': 'drugstores', 'name': 'Аптека'}], 'Hours': {'text': 'ежедневно, круглосуточно', 'Availabilities': [{'TwentyFourHours': True, 'Everyday': True}]}}}}, {'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [37.562981, 55.745607]},
# 'properties': {'name': 'ГорЗдрав', 'description': 'Большая Дорогомиловская ул., 1, Москва, Россия', 'boundedBy': [[37.5588755, 55.74329093], [37.5670865, 55.74792293]], 'CompanyMetaData': {'id': '1020095219', 'name': 'ГорЗдрав', 'address': 'Россия, Москва, Большая Дорогомиловская улица, 1', 'url': 'http://gorzdrav.org/', 'Phones': [{'type': 'phone', 'formatted': '+7 (499) 653-62-77'}, {'type': 'phone', 'formatted': '+7 (495) 797-63-36'}, {'type': 'phone', 'formatted': '+7 (499) 653-62-67'}], 'Categories': [{'class': 'drugstores', 'name': 'Аптека'}], 'Hours': {'text': 'ежедневно, 8:00–23:00', 'Availabilities': [{'Intervals': [{'from': '08:00:00', 'to': '23:00:00'}], 'Everyday': True}]}}}}]}

