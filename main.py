from src.calculator import Calculator
from services_mapper import services_logics, config


if __name__ == '__main__':
    # На вход подается конфигурация в виде словаря или json и
    # словарь функций бизнес-логики, где для каждого параметра каждого сервиса
    # указана соответствующая функция
    # Указываем именованные входные параметры. Они должны быть названы в соответствие
    # с названием входных параметров в функциях бизнес-логики
    calculator = Calculator(config, services_logics)
    updated_config = calculator.update_config(agents=100, storage=4.67, traffic=7.342, mail_traffic=31.23, distributed=True, nodes=230)
    print(updated_config)
    updated_config = calculator.update_config(agents=100, mail_traffic=12.3, distributed=True)
    calculator.update_config()


