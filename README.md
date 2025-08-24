# Система учёта заказов
Прототип промышленной системы учёта заказов, клиентов и
товаров с графическим интерфейсом, базой данных и возможностью анализа данных.
## Возможности
- графический интерфейс на tkinter
- регистрация клиентов и их контактных данных
- управление заказами и связанными товарами
- визуализированные анализ данных - динамика продаж, топ 5 товаров, связь клиентов с продуктами, которые они заказывали
- экспорт и импорт данных в/из различных форматов (CSV, JSON)
- хранение данных в локальной базе данных SQLite (shop.db)

## Описание модулей
FinalCertification/main.py : Главный файл для запуска приложения.
FinalCertification/models.py : Определяет классы данных - Client, Product, Order
FinalCertification/db.py : Отвечает за взаимодействие с базой данных SQLite, импорт и экспорт данных.
FinalCertification/gui.py : Содержит код графического интерфейса, созданного с помощью tkinter
FinalCertification/analysis.py : Содержит анализ данных и визуализацию с помощью pandas, matplotlib, networkx
FinalCertification/tests.py :unit-тесты для модулей models и analysis

## Установка и запуск
1. Клонируйте репозиторий: 
    ```bash
    git clone https://github.com/mrdog2009/FinalCertification
    cd FinalCertification
    ```

2. Создайте и активируйте виртуальное окружение:
    ```bash
    python -m venv venv
    # Для Windows:
    venv\Scripts\activate
    # Для macOS/Linux:
    source venv/bin/activate
    ```

3. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```
4. Запустите приложение:
    ```bash
    python -m FinalCertification.main
    ```

## Запуск тестов
    ```bash
    python -m unittest discover tests
    ```


## Генерация документации
Для генерации документации с помощью Sphinx:
1. Установите Sphinx (он уже должен быть в "requirements.txt").
2. Перейдите в папку "docs" и запустите быструю настройку:
    ```bash
    cd docs
    sphinx-quickstart
    ```

    (Hа большинства вопросов можно отвечать "Enter", но укажите путь к вашему проекту "…/FinalCertification')
3. Отредактируйте файл "docs/conf.py", раскомментировав и настроив следующие строки:
    ```python
    import os
    import sys
    sys.path.insert(0,os.path.abspath('…'))
    
    extensions = [
        'sphinx.ext.autodoc',
        'sphinx.ext.napoleon', # для поддержки numpydoc
    ]
    ```
4. Сгенерируйте HTML-документацию:
    ```bash
    make html
    ```
    Готовая документация будет находиться в "docs/_build/html/index.html".

## Скриншоты