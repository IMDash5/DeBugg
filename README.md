# DeBugg
### IT-проект по программе "Цифровое моделирование и суперкомпьютерные технологии"
## ResumeAI
### ResumeAI — это инновационный проект, который использует нейронные сети для автоматического анализа резюме. Проект направлен на упрощение составления резюме, поиск ключевых ошибок и предложение рекомендаций для людей в поисках работы.
## Содержание
- [Технологии](#технологии)
- [Начало работы](#начало-работы)
- [Разработка](#разработка)
- [Команда проекта](#команда-проекта)
- [Ссылки](#ссылки)

## Технологии
Проект разработан с использованием современных технологий и инструментов:

- Фронтенд:
    - [GatsbyJS](https://www.gatsbyjs.com/) — генератор статических сайтов.
    - [TypeScript](https://www.typescriptlang.org/) — строго типизированный JavaScript.
    - [Tailwind CSS](https://tailwindcss.com/) — CSS-фреймворк для быстрой разработки интерфейсов и адаптивной верстки.
- Бэкенд:
    - [FastAPI](https://fastapi.tiangolo.com) — современный фреймворк для создания API.
    - [Python](https://www.python.org/) — язык программирования для бэкенда.
    - [Poetry](https://python-poetry.org/) — инструмент для управления зависимостями Python.
    - [SQLAlchemy](https://www.sqlalchemy.org) - инструмент для синхронизации объектов Python и записей реляционной базы данных.
    - [PosrgreSQL](https://www.postgresql.org) - свободная объектно-реляционная система управления базами данных (СУБД).
- ML:
    - [TensorFlow](https://www.tensorflow.org/) — библиотека для машинного обучения.
    - [PyTorch]() — фреймворк машинного обучения для языка Python с открытым исходным кодом, созданный на базе Torch.
    - [Scikit-learn](https://scikit-learn.org/) — библиотека для машинного обучения.

## Начало работы
### Требования

Для установки и запуска проекта необходимы следующие инструменты:

- [Node.js](https://nodejs.org/) v14+
- [Python](https://www.python.org/) v3.9+
- [Poetry](https://python-poetry.org/) для управления зависимостями Python.
- [Git](https://git-scm.com/) для клонирования репозитория.

### Установка зависимостей
1. Клонируйте репозиторий:
```sh
git clone https://github.com/IMDash5/DeBugg
```
2. Установите зависимости для фронтенда:
```sh
cd frontend
npm install
```
3. Установите Tailwind CSS:
```sh
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```
4. Настройте Tailwind, добавив в `src/index.css`:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```
5. Установите зависимости для бэкенда:
```sh
cd backend
poetry install
```
### Запуск Development сервера
1. Запустите фронтенд:
```sh
cd frontend
npm run dev
```
2. Запустите бэкенд:
```sh
cd backend
poetry run python -m backend.server
```
3. Откройте браузер и перейдите по адресу:
- Фронтенд: http://localhost:3000
- Бэкенд: http://localhost:8000
## Разработка
- frontend/:
    - Содержит исходный код фронтенда на GatsbyJS.
- backend/:
    - Содержит исходный код бэкенда на FastAPI.
- ML/:
    - Содержит модели машинного обучения и скрипты для их обучения.
## Команда проекта
- [Чувилов Александр Александрович М8О-213Б-23](https://github.com/CHUVISS) — Frontеnd-разработчик, Тимлид.
- [Петров Марк Алексеевич М8О-213Б-23](https://github.com/Mark-Petrov) - Frontеnd-разработчик, UI/UX -дизайнер.
- [Арсельгов Адам Бесланович М8О-213Б-23](https://github.com/adamarselgov2609) - Frontеnd-разработчик.
- [Миронов Данил Алексеевич М8О-214Б-23](https://github.com/al1vel) - Frontend-разработчик, помощник писателя.
- [Чечина Лилия Алексеевна М8О-201Б-23](https://github.com/Lilia-Chechina) - Технический писатель.
- [Евтенко Никита Александрович М8О-201Б-23](https://github.com/Neochiter22) – Data-Engineer.
- [Маврин Иван Дмитриевич М8О-201Б-23](https://github.com/IMDash5) - Заместитель, Ответственный за Backend, Backend-разработчик.
- [Червоненко Павел Юрьевич М8О-214Б-23](https://github.com/pavelchervonenko) - ML-Engineer.
- [Гусев Савелий Вячеславович М8О-214Б-23](https://github.com/guse95) - Backend-разработчик.
- [Заворотный Алексей Александрович М8О-214Б-23](https://github.com/AlekseiZavorotnyi) - Backend-разработчик.
- [Кауров Данил Николаевич М8О-201Б-23](https://github.com/KaurDanil) – Data-Engineer.

## Ссылки
- [Trello](https://trello.com/b/BPCEQxoc/debugg-gpt) -  сервис для управления задачами.
- [Miro](https://miro.com/app/board/uXjVMrOehiU=/) - архитектура проекта.