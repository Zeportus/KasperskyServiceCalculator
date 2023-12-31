# KasperskyServiceCalculator
## Установка
Чтобы установить сервис - склонируйте себе этот репозиторий.  
Сам сервис представлен в папке src.  
Остальное - это тесты и пример работы с сервисом (Решение поставленной задачи в тестовом задании).

## Запуск
После клонирования просто запустите main.py, это создаст вам текстовый файл в формате json.  
В нем будет представлена новая конфигурация сервисов, которая представлена в business_logics.  
Сама конфигурация и разметка функций бизнес-логики, необходимая для калькулятора, находится в  
services_mapper.py

## Бизнес-логика
Для начала вам потребуется описать бизнес-логику для параметров своих сервисов.  
Пример этого можно посмотреть в business_logics.  
  
Для описания бизнес логики вам потребуется импортировать декоратор, который требуется для каждой функции.  
В него надо передавать название входных параметров, потом эти же названия используются в параметрах самой функции.
Их может быть несколько или может не быть вовсе
```python
import math
from src.calculator import used_parameters

@used_parameters('traffic_mb')
def service1_enabled(traffic_mb) -> bool:
    return traffic_mb > 0

@used_parameters('disk_storage_MB')
def service1_nodes(disk_storage_MB) -> int:
    return math.ceil(disk_storage_MB / 10000)

@used_parameters()
def service1_cpu_cores() -> int:
    return 5
```

## Разметка бизнес-логики
После создания функций вам потребуется создать разметку в в виде словаря следующего вида:
```python
services_logic = {
    'service_1': {
        'enabled': service1_enabled,
        'nodes': service1_nodes,
        'cpu_cores': service1_cpu_cores,
        'memory': service1_memory,
    }, 

    'service_2': {
        'enabled': service2_enabled,
        'nodes': service2_nodes,
        'cpu_cores': service2_cpu_cores,
        'memory': service2_memory
    }
}
```
В качестве значений для каждого параметра просто выступают ссылку на необходимые функции, больше ничего не требуется.  
Главное указывайте для своих функций декоратор и калькулятор будет корректно отрабатывать  
  
Заполнять разметку для всех сервисов или всех параметров каждого сервиса - необязательно. Вы можете указать функции-бизнес логики  
только для тех, которые необходимы. Остальные значения из конфигурации при этом просто будут оставаться без изменений.  
НО! Вы не можете добавлять в разметку те сервисы и те параметры этих сервисов, которые не указаны в изначальной конфигурации.  
В этом случае программа будет выкидывать исключения.

## Создание объекта калькулятора
После того как вы подготовили свою бизнес-логику и разметили ее - настала пора создавать объект:
```python
config = {
        "service_1": {
            "enabled": False,
            "nodes": 0,
            "cpu_cores": 0,
            "memory": 0
        },

        "service_2": {
            "enabled": True,
            "nodes": 10,
            "cpu_cores": 12,
            "memory": 100,
            'add_field': 'str',
            'in_field': {
                'list': [2, 3, 5],
                'num': 500
            },
            'another': 3.55
        }
    }

only_params = ['disk_storage_MB', 'traffic_mb']
calculator = Calculator(config, services_logic, only_params)
updated_config = calculator.update_config(disk_storage_MB=100, traffic_mb=200)
```
Здесь service_logic это разметка бизнес-логики для config.  
У калькулятора есть необязательный параметр only_params. Он требуется для проверки переданных в 
в метод update_config параметров. Если вам нужно всегда передавать одни и те же параметры, то лучше  
использовать это, ведь это исключит возможность опечатки.  
  
Без этого параметра вы сможете передавать любое количество аргументов и любое имя, но калькулятор будет  
обращать внимания только на те, что были указаны в функциях бизнес-логики.  
Если вы передаете не все параметры, то функции, которые их требуют - будут просто проигнорированы и останутся  
значения по умолчанию. Калькулятор отработает без ошибок.
