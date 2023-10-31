from copy import deepcopy

# Класс ошибки, который выводит название проблемного сервиса или 
# название проблемного параметра и сервиса, а далее сообщает, что
# в словаре функций бизнес-логики есть то, чего нет в обычном конфиге - 
# это нарушение логики
class ConfigError(Exception):
    def __init__(self, text) -> None:
        super().__init__(f'{text} is present in services_logic, but not in Calculator config')

class Service:
    def __init__(self, name: str, config: dict) -> None:
        self.name = name
        # Выполняем здесь глубокое копирование, так как иначе переданный конфиг 
        # тоже будет меняться.
        self._config = deepcopy(config)
    
    def set_service_funcs(self, logic_funcs: dict) -> None:
        self._service_funcs = logic_funcs
    
    # При обновление параметров сервиса данный метод перебирает
    # параметры и привязанные к ним функции бизнес логики.
    # Если декоратор в результате вернул None, а не функцию бизнес-логики, 
    # то игнорируем эту функцию, так как для нее не был передан необходимый параметр 
    # Обновляем конфиг через буффер, чтобы не влиять на изначальный конфиг
    def update_config(self, **kwargs) -> None:
        buffer = deepcopy(self._config)
        for param, logic_func in self._service_funcs.items():
            if param not in buffer:
                raise ConfigError(f'"{param}" of "{self.name}"')
            
            result = logic_func(**kwargs)
            if result is None: continue
            buffer[param] = result
        
        return buffer