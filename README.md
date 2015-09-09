# README

Гайд для запуска тестового задания. Нам необходимо два терминала.

1.  Открываем терминал #1. Копируем в нужную папку репозиторий и заходим в него.

        $ git clone https://github.com/yeahframeoff/skein-test-task.git yefremov-task
        $ cd yefremov-task

2.  Создаем в папке на один уровень выше виртуальное окружение и указываем Python3 в качестве образца

        $ cd ..
        $ virtualenv  --no-site-packages --distribute -p python3 yefremov
        $ ./yefremov/scripts/activate.sh
        (yefremov)$ cd yefremov-task

3.  Устанавливаем необходимые пакеты:

        (yefremov)$ pip install -r requirements.txt

4.  Применяем миграции и импортируем данные:

        (yefremov)$ python manage.py migrate
        (yefremov)$ python manage.py loaddata "book_store/book_data.json"

5.  Запускаем сервер:

        (yefremov)$ python manage.py runserver 7000

6.  В терминале #2 переходим в папку с проектом и тоже активируем виртуальное окружение:

        $ cd /path/to/yefremov-task
        $ ../yefremov/scripts/activate.sh

7.  Там же запускаем наш брокер сообщений:

        (yefremov)$ celery -A skein_testtask worker --loglevel=info

8.  В браузере открываем запущенный сайт ([localhost:7000] (http://localhost:7000))

    ![Запущенный сайт](http://i.imgur.com/umyPxax.png "Запущенный сайт")

9.  Вводим интересующие нас параметры поиска, нажимаем "Поиск" и переходим в терминал #2. 
В течение нескольких секунд должно появиться письмо с результатами поиска. 
Для простоты проверки был использован консольный бекенд Django для отправки email.

10. Для проверки данных создадим пользователя админки:
        
        (yefremov)$ python manage.py createsuperuser 

    Выберите подходящие для вас логин, email и пароль
    После этого переходим в админку ([localhost:7000/admin] (http://localhost:7000/admin)) и вводим входные данные
    вновь созданного администратора.


## Примечание

В папке `book_import` находится текст тестовой книги `hobbit.txt` и скрипт для импорта книги в библиотеку `hobbit_to_fixture.py` (скрипт не создает фикстуры, а сохраняет импортированные данные в БД).

Для импорта использовалась следующая команда:

    (yefremov)$ python manage.py shell
    ...
    >>> execfile('hobbit_to_fixture.py')
    ...
    >>> exit()
