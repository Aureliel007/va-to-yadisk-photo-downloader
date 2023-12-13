import requests
import json
from urllib.parse import urlencode
import os

def get_token():
    app_id = '51812835'
    base_url = 'https://oauth.vk.com/authorize'
    params = {
        'client_id': app_id,
        'redirect_uri': 'https://oauth.vk.com/blank.html',
        'display': 'page',
        'scope': 'photos',
        'response_type': 'token'
    }

    oauth_url = f'{base_url}?{urlencode(params)}'
    print(f'Перейдите по ссылке и скопируйте токен: {oauth_url}')
    token = input('Введите полученный токен: ')
    return token

class VkPhotosDownloader:

    def __init__(self, access_token, user_id, version='5.199'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}
        self.base_url = 'https://api.vk.com/method/'

    def get_photos(self, count=5):
        url = self.base_url
        params = self.params
        params.update({
            'owner_id': self.id,
            'album_id': 'profile',
            'rev': 1,
            'extended': 1,
            'count': count
        })
        response = requests.get(f'{url}photos.get', params=params)
        if 200 <= response.status_code < 300:
            return response.json()
    
    def download_photos(self, count=5):
        '''
        Функция принимает в качестве параметра количество фотографий,
        по умолчанию скачается 5 последних фото.
        Функция возвращает словарь с названиями файлов и их типами размеров
        для дальнейшего использования при выгрузке в Яндекс диск
        и формирования итогового отчета.
        '''
        if not os.path.exists('vk_photos'):
            os.mkdir('vk_photos')
        data = self.get_photos(count)
        file_names = {} # в этот словарь будут сохраняться имена файлов и тип размера

        for item in data['response']['items']:
            max_width = 0

            for size in item['sizes']:
                width = size.get('width', 0)
                if width > max_width:
                    download_url = size['url']
                    size_type = size.get('type', '')

            file_name = f"{item['likes']['count']}.jpg"
            if file_name in file_names:
                file_name = f"{item['likes']['count']}_{item['date']}.jpg"

            file_names.update({file_name: size_type})

            response = requests.get(download_url)
            if 200 <= response.status_code < 300:
                path = os.path.join('vk_photos', file_name)
                with open(path, 'wb') as file:
                    file.write(response.content)
        
        return file_names
            
class YaDiskUploader:
    def __init__(self, ya_access_token, photos_names):
        self.headers = {'Authorization': ya_access_token}
        self.base_url = 'https://cloud-api.yandex.net/'
        self.photos = photos_names

    def create_folder(self):
        url_create_folder = self.base_url + 'v1/disk/resources'
        params_dict = {
            'path': 'Vk_photos'
        }
        response = requests.put(url_create_folder, params=params_dict, headers=self.headers)
        return f"{params_dict['path']}"
    
    def upload_photos(self):
        folder_path = self.create_folder()
        photos = self.photos
        request_url = self.base_url + 'v1/disk/resources/upload'
        report = []
        for photo in photos:
            path = f"{folder_path}/{photo}"
            params = {
                'path': path,
                'overwrite': True
            }
            response = requests.get(request_url, params=params, headers=self.headers)
            url = response.json().get('href')
            file_path = os.path.join('vk_photos', photo)
            with open(file_path, 'rb') as file:
                response = requests.put(url, files={'file': file})
                report.append({'file_name': photo, 'size': photos[photo]})
        
        with open('report.json', 'w') as file:  # Отчет о загрузке будет записан в файл
            json.dump(report, file, indent=4)


access_token = get_token()
user_id = input('Введите свой VK user ID: ')
ya_access_token = 'OAuth ' + input('Введите свой токен для получения доступа к Яндекс Диску: ')
vk = VkPhotosDownloader(access_token, user_id)
photos_names = vk.download_photos()
ya = YaDiskUploader(ya_access_token, photos_names)
ya.upload_photos()
