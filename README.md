# FLASK DOVHALIUK

## Перший запуск
1. Змініть дані в to_renamed.env та перейменуйте файл
2. Розгорніть Docker
  - в файлі docker-compose.yml змініть значення change_me на свої
  - перейдіть в папку з файлом docker-compose.yml та запустіть в консолі
```
docker-compose up --build
```
3. Встановіть бібліотеки
```
pip install -r requirements.txt
```
4. В файлі .env змініть IS_FIRST_START=1 та запустіть start.py. Після додавання ви зможете перевірити наявність елементів
5. В файлі .env змініть IS_FIRST_START=0


## Запуск кода
Запустіть файл start.py


## Запити
### GET Products
```
/products/ID_PRODUCT?page=NUMB_PAGE
```
### PUT Review
```
/add_review

{
  "Product ID": "1",
  "Title": "Title Text",
  "Review": "Review Text"
}

```


## Увага
- Працює Redis-кешування (REDIS_TTL в .env), тому значення не будуть оновлюваться одразу (за замовчуванням кеш видаляється через 20 секунд)
