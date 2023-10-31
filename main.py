from src.calculator import Calculator
from services_mapper import services_logics, config

if __name__ == '__main__':
    # На вход подается конфигурация в виде словаря или json и
    # словарь функций бизнес-логики, где для каждого параметра каждого сервиса
    # указана соответствующая функция
    # Указываем именованные входные параметры. Они должны быть названы в соответствие
    # с названием входных параметров в функциях бизнес-логики.
    # Для предупреждения опечаток при передаче параметров в при обновлении конфигурации -
    # можно в конструктор калькулятор передать список всех параметров, которые будут использованы
    # Если какой-то не передастся или передастся дополнительный или с другим именем -
    # вызовется исключение
    only_params = ['agents', 'storage', 'traffic', 'mail_traffic', 'distributed', 'nodes']
    calculator = Calculator(config, services_logics, only_params)
    updated_config = calculator.update_config(storage=4.67, traffic=7.342, mail_traffic=31.23, distributed=True, nodes=230, agents=100)
    # Строчка ниже вызовет ошибку, так как у нас установлен only_params    
    # updated_config = calculator.update_config(agents=100, mail_traffic=12.3, distributed=True)


