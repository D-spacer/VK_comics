# VK_comics
Публикует случайный комикс с сайта https://xkcd.ru/ в ваше сообщество Vkontakte.

### Установка

Для установки пакета склонируйте его из репозитория с помощью команды

```git clone https://github.com/D-spacer/VK_comics.git```

Проверить установленные пакеты можно с помощью команды `pydoc modules`.

### Зависимости
Для работы скрипта потребуется создать собственное приложение Vkontakte и отправить запрос на получение необходимых прав, для этого воспользуйтесь следующей инструкцией: https://pechenek.net/social-networks/vk/api-vk-sozdayom-standalone-prilozhenie-i-poluchaem-token/
Учтите, что указывать необходимо ID вашего приложения, а в параметре scope нужно указать права groups,wall,images
Полученный токен укажите в файле .env в следующем виде:

```ACCESS_TOKEN=<токен>```

Сюда же внесите ID вашей группы, куда вы будете публиковать комиксы:

```GROUP_ID=<токен>```

Кроме того для работы необходимы определенные пакеты, такие как `requests`.
Установить пакеты, необходимые для работы программы, можно с помощью команды: 

```pip install -r requirements.txt```

### Запуск скрипта

Скрипт можно запустить через среду программирования или консоль с помощью команды

```python main.py```
