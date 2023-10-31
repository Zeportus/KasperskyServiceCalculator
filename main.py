from src.calculator import Calculator
from business_logics.example_logic import services_logic, services_logic1


if __name__ == '__main__':
    config = {
        "service_1": {
            "enabled": False,
            "nodes": 0,
            "cpu_cores": 0,
            "memory": 0,
            'left': 'shit',
            'in': {
                'func1': 0,
                'in1': {
                'func2': 0,
                'static': 100,
                'in2': {
                    'func3': 0,
                    'func4': 0
                }
                }, 
                'in2': {
                    'func6': 0
                }
            },
            'in1': {
                'in2': {
                    'func5': 0
                }
            }
        },

        "service_2": {
            "enabled": True,
            "nodes": 10,
            "cpu_cores": 12,
            "memory": 100
        }

    }
    
    # На вход подается конфигурация в виде словаря или json и
    # словарь функций бизнес-логики, где для каждого параметра каждого сервиса
    # указана соответствующая функция
    calculator = Calculator(config, services_logic)
    # Указываем именованные входные параметры. Они должны быть названы в соответствие
    # с названием входных параметров в функциях бизнес-логики
    updated_config = calculator.update_config(traffic_mb=100, disk_storage_MB=100)
    print(config)
    print(updated_config)
    # calculator.update_services_logic(services_logic1)
    # updated_config = calculator.update_config(traffic_mb=100, disk_storage_MB=100)
    # print(updated_config)

