# Программа для резервного копирования фотографий профиля VK в Яндекс Диск

## Для начала работы требуется:
1. Заполнить файл settings.yaml.example:
   - В поле "vk_token" ввести токен, полученный по [ссылке](https://oauth.vk.com/authorize?client_id=51812835&redirect_uri=https%3A%2F%2Foauth.vk.com%2Fblank.html&display=page&scope=photos&response_type=token)
   - В поле "ya_disk_token" ввести токен, полученный по [ссылке](https://yandex.ru/dev/disk/poligon/)
2. Переименовать файл settings.yaml.example в settings.yaml

## Возможности программы
1. Скачивание фотографий профиля на жесткий диск.
2. По умолчанию будет загружено 5 последний фото, но количество можно задать при вызове функции.
3. Выгрузка фотографий в отдельную директорию на Яндекс Диске.