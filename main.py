import requests
import json
from datetime import datetime
from tqdm import tqdm


def get_token(user):
    if isinstance(user, VkUser):
        with open('vk_token.txt', 'r') as file_object:
            vk_token = file_object.read().strip()
        return vk_token
    elif isinstance(user, YaUploader):
        with open('ya_token.txt', 'r') as file_object:
            ya_token = file_object.read().strip()
        return ya_token
    else:
        return None


def create_json(list_photos):
    json_file = []
    for photo in list_photos:
        del photo['url']
        json_file.append(photo)
    with open('info.json', 'w', encoding='utf-8') as f:
        json.dump(json_file, f, ensure_ascii=False, indent=1)
    print('Файл info.json создан.')


class VkUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, version):
        self.token = get_token(self)
        self.version = version
        self.params = {
            'access_token': self.token,
            'v': self.version
        }

    def get_id(self, username):
        get_id_url = self.url + 'users.get'
        get_id_params = {'user_ids': username}
        res = requests.get(get_id_url, params={**self.params, **get_id_params})
        res = res.json()
        if res.get('error') is not None:
            print('Ошибка 113! Неверный идентификатор пользователя')
            return None
        else:
            return res['response'][0].get('id')

    def get_profile_photos(self, user_id, count=5):
        if user_id.isdigit():
            user_id = int(user_id)
        else:
            user_id = self.get_id(user_id)
            if user_id is None:
                return None
        album = input('''Введите с какого альбома вы хотите скачать фото:
            1 - фото профиля
            2 - фото со стены
            3 - сохраненные фото
            ''')
        album_id = {
            '1': 'profile',
            '2': 'wall',
            '3': 'saved'
        }
        profile_photos_url = self.url + 'photos.get'
        profile_photos_params = {
            'owner_id': user_id,
            'album_id': album_id[album],
            'extended': 1,
            'photo_sizes': 1,
            'count': count
        }
        res = requests.get(profile_photos_url, params={**self.params, **profile_photos_params})
        res = res.json()
        if res.get('error') is not None:
            print('Ошибка! Пользователь не найден')
            return None
        res = res['response']['items']
        list_photos = []
        list_name = []
        for item in res:
            dict_photos = {}
            max_width = 0
            photo_url = ''
            photo_type = ''
            if str(item['likes']['count']) + '.jpg' in list_name:
                list_name.append(str(item['likes']['count']) + '-' + datetime.utcfromtimestamp(item['date']).strftime(
                    '%Y-%m-%d') + '.jpg')
                dict_photos['file_name'] = str(item['likes']['count']) + '-' + datetime.utcfromtimestamp(
                    item['date']).strftime('%Y-%m-%d') + '.jpg'
            else:
                list_name.append(str(item['likes']['count']) + '.jpg')
                dict_photos['file_name'] = str(item['likes']['count']) + '.jpg'
            for size in item['sizes']:
                if size['width'] > max_width:
                    photo_url = size['url']
                    photo_type = size['type']
            dict_photos['size'] = photo_type
            dict_photos['url'] = photo_url
            list_photos.append(dict_photos)
        return list_photos


class YaUploader:

    def __init__(self, list_photos):
        self.list_photos = list_photos
        self.token = get_token(self)

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def create_folder(self, name):
        folder_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        params = {'path': '/' + name}
        response = requests.put(folder_url, headers=headers, params=params)
        if response.status_code == 201:
            print(f'Папка {name} создана')
        else:
            print('Ошибка')
        return name

    def upload(self):
        if self.list_photos is None:
            print('Фото не найдены, загрузка не удалась!')
            return None
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        list_photos = self.list_photos
        name_folder = input('Введите название папки: ')
        self.create_folder(name_folder)
        print(f'Загружаем фотографии в папку {name_folder} на Яндекс.Диск...')
        for photo in tqdm(list_photos):
            params = {'url': photo['url'], 'path': name_folder + '/' + photo['file_name']}
            href = upload_url
            response = requests.post(href, headers=headers, params=params)
            response.raise_for_status()
        print('Фотографии загружены на Яндекс.Диск.')
        create_json(list_photos)


if __name__ == "__main__":
    vk_client = VkUser('5.131')
    user_ids = input('Введите id пользователя или его username: ')
    count_photo = int(input('Введите количество загружаемых фото: '))
    photo_list = vk_client.get_profile_photos(user_ids, count_photo)
    yadisk = YaUploader(photo_list)
    yadisk.upload()
