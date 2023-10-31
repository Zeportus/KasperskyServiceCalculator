from src.service import Service, ConfigError
import json


class Calculator:
    def __init__(self, config: dict | str, services_logic: dict, only_params: list=[]) -> None:
        # Определенные для передачи входные параметры.
        # Если не задавать, то передавать можно любые параметры
        # Сортируем сразу, чтобы потом сортировать только переданные
        # ключи и сравнивать
        self._only_params = sorted(only_params)
        if isinstance(config, str):
            config = json.loads(config)
        
        # Создаем словарь сервисов и заполняем его в соответствие с конфигурацией
        self.services: dict[str, Service] = {}
        for service_name in config:
            self.services[service_name] = Service(service_name, config[service_name])
        
        # Обновляем функции бизнес-логики для сервисов
        self.update_services_logic(services_logic)
    
    def update_config(self, **kwargs) -> dict:
        # Если установлены обязательные параметры и были переданы
        # какие-то дополнительные, либо не переданы нужные в полном объеме
        # параметры, тогда ошибка 
        if self._only_params and sorted(list(kwargs.keys())) != self._only_params:
            raise Exception(f'You have set only_params, but not gave them. Your only params: {self._only_params}')
            
        buffer = {}
        # При обновлении конфига вызываем метод обновления для каждого сервиса,
        # передавая все именованные параметры.
        for service_name, service in self.services.items():
            buffer[service_name] = service.update_config(**kwargs)

        with open('services_config.json', 'w') as f:
            json.dump(buffer, f, indent=4)

        return buffer
    
    # Функция обновляет бизнес-логику для сервисов. Если начальный конфиг не изменяется, 
    # то нет нужды создавать новый экземпляр калькулятора, можно передать новую логику через этот метод
    # таким же образом как он передавался в __init__. При этом следует учитывать, что сервисы и их параметры, которые
    # находятся в services_logic обязательно должны быть в изначальном конфиге, иначе бы это нарушило логику.
    # Но обратное допустимо. services_logic может быть вовсе пустым или содержать не все параметры сервиса из конфига
    def update_services_logic(self, services_logic: dict) -> None:
        for service_name, logic_funcs in services_logic.items():
            if service_name not in self.services:
                raise ConfigError(service_name)
            self.services[service_name].set_service_funcs(logic_funcs)

# Это декоратор, который проверяет были ли переданы в метод Calculator.update_config
# требуемые параметры для функции бизнес-логики. Если требуемый параметр не был передан, 
# то игнорируем фукнцию бизнес-логики и оставляем привязаный к ней параметр был изменений.
# В ином случае заполняем буфферный словарь, чтобы в бизнес-логику передать только нужные параметры
# Это позволяет красиво писать функции для бизнес-логики :)
def used_parameters(*params_names):
    def wrapper(func):
        def output_func(**kwargs):
            correct_params = {}
            for param_name in params_names:
                if param_name not in kwargs:
                    return None
                else:
                    correct_params[param_name] = kwargs[param_name]
                
            return func(**correct_params)
        return output_func
    return wrapper