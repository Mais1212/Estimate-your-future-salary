# ENUMIRATE YOUR SALARY

Скрипт парсит вакансии програмистов через [HeadHunter API](https://api.hh.ru/vacancies) и
[SuperJob]("https://api.superjob.ru/2.0/vacancies/"), после результаты парсинга выводятся в консоль в виде таблицы.
Учитываются только вакансии по Москве и опубликованные меньше месяца назад. Список языков программирования, по которым собираются и выводятся данные:
-   JavaScript
-   Java
-   C#
-   Python
-   Ruby
-   Go
-   PHP
-   C++
-   Swift

### Пример результата
Такой вывод будет в консоли :
```
┌SuperJob───────────────┬──────────────────┬─────────────────────┬──────────────────┐
│ Язык программирования │ Вакансий найдено │ Вакансий обработано │ Средняя зарплата │
├───────────────────────┼──────────────────┼─────────────────────┼──────────────────┤
│ javascript            │ 104              │ 75                  │ 129618           │
│ Java                  │ 40               │ 24                  │ 144770           │
│ C#                    │ 30               │ 22                  │ 151664           │
│ Python                │ 75               │ 42                  │ 141666           │
│ Ruby                  │ 8                │ 5                   │ 166800           │
│ Go                    │ 227              │ 224                 │ 124831           │
│ PHP                   │ 88               │ 58                  │ 122420           │
│ C++                   │ 32               │ 25                  │ 146840           │
│ Swift                 │ 8                │ 3                   │ 185833           │
└───────────────────────┴──────────────────┴─────────────────────┴──────────────────┘
┌HeadHunter─────────────┬──────────────────┬─────────────────────┬──────────────────┐
│ Язык программирования │ Вакансий найдено │ Вакансий обработано │ Средняя зарплата │
├───────────────────────┼──────────────────┼─────────────────────┼──────────────────┤
│ javascript            │ 4053             │ 879                 │ 161499           │
│ Java                  │ 3525             │ 464                 │ 198412           │
│ C#                    │ 1653             │ 449                 │ 160849           │
│ Python                │ 4742             │ 520                 │ 170130           │
│ Ruby                  │ 314              │ 95                  │ 194942           │
│ Go                    │ 1141             │ 315                 │ 152067           │
│ PHP                   │ 1808             │ 848                 │ 143263           │
│ C++                   │ 1718             │ 514                 │ 162751           │
│ Swift                 │ 577              │ 145                 │ 198262           │
└───────────────────────┴──────────────────┴─────────────────────┴──────────────────┘
```

### Как указать токен SJ
- Зарегистрируйте приложение на [SuperJob](https://www.superjob.ru/auth/login/?returnUrl=https://api.superjob.ru/register/)
- Получить ваш уникальный токен
- Создайте файл `.env`
- Указать в файле `.env` переменную :
```python
SUPER_JOB_KEY=<Ваш уникальный токен>
```

### Как установить
Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```
### Пример запуска скрипта
```
python main.py
```
