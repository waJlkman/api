Задание на дипломный проект «Резервное копирование» первого блока «Основы языка программирования Python».
----
Возможна такая ситуация, что мы хотим показать друзьям фотографии из социальных сетей, но соц. сети могут быть недоступны по каким-либо причинам. Давайте защитимся от такого.
Нужно написать программу для резервного копирования фотографий с профиля(аватарок) пользователя vk в облачное хранилище Яндекс.Диск.
Для названий фотографий использовать количество лайков, если количество лайков одинаково, то добавить дату загрузки.
Информацию по сохраненным фотографиям сохранить в json-файл.

# Задание:
Нужно написать программу, которая будет:

1. Получать фотографии с профиля. Для этого нужно использовать метод [photos.get.](https://vk.com/dev/photos.get)
1. Сохранять фотографии максимального размера(ширина/высота в пикселях) на Я.Диске.
1. Для имени фотографий использовать количество лайков.
1. Сохранять информацию по фотографиям в json-файл с результатами.
### Входные данные:
Пользователь вводит:

1. id пользователя vk;
1. токен с [Полигона Яндекс.Диска](https://yandex.ru/dev/disk/poligon/). Важно: Токен публиковать в github не нужно!
### Выходные данные:
1. json-файл с информацией по файлу:

        [{
        "file_name": "34.jpg",
        "size": "z"
        }]
        
1. Измененный Я.диск, куда добавились фотографии.​​
### Обязательные требования к программе:
1. Использовать REST API Я.Диска и ключ, полученный с полигона.
1. Для загруженных фотографий нужно создать свою папку.
1. Сохранять указанное количество фотографий(по умолчанию 5) наибольшего размера (ширина/высота в пикселях) на Я.Диске
1. Сделать прогресс-бар или логирование для отслеживания процесса программы.
1. Код программы должен удовлетворять PEP8.​
### Необязательные требования к программе:
1. Сохранять фотографии и из других альбомов.
1. Сохранять фотографии из других социальных сетей. [Одноклассники](https://apiok.ru/) и [Инстаграмм](https://www.instagram.com/developer/)
1. Сохранять фотографии на Google.Drive.
Советы:

1. Для тестирования можно использовать аккаунт https://vk.com/begemot_korovin
1. Токен для VK api: 958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008
