# Data Engineer tasks

## How to

### Установка Docker + Docker Compose

Docker: https://docs.docker.com/engine/install/  
Docker Compose (Linux): https://docs.docker.com/compose/install/

### Запуск окружения для тестового задания

В командной строке:

```sh
cd path/to/task/folder
docker-compose up -d --build
```

После выполнения команд тестовое задание будет доступно через браузер в виде Jupyter Notebook по адресу http://localhost:8888/tree/work

Пароль от Jupyter Notebook: `test2021`

Результатом выполнения задания будет файл Jupyter Notebook `Task.ipynb` с кодом и результатами выполнения задания.
