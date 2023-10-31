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
        # Неизменяемый словарь, в котором лежит изначальный конфиг сервиса.
        # Требуется для сброса посчитанных атрибутов при обновлении словаря 
        # с функциями бизнес-логики
        self._imtbl_config = deepcopy(config)
        # Выполняем здесь глубокое копирование, так как иначе переданный конфиг 
        # тоже будет меняться.
        self._config = deepcopy(config)
        # Это поле требуется для работы рекурсии. В него заносятся вложенные 
        # элементы словаря _config, чтобы была возможность работать с ними, но
        # при этом не терять ссылку на весь конфиг
        self._prev_dict = self._config
    
    def set_service_funcs(self, logic_funcs: dict) -> None:
        # _service_funcs содержит словарь с параметрами и их фукнциями бизнес-логики
        # _recursion_funcs требуется также для работы рекурсии. Работает по аналогии с 
        # _prev_dict, но для _service_funcs
        self._service_funcs = logic_funcs
        self._recursion_funcs = logic_funcs
    
    # При получении конфига необходимо сбрасывать вспомогательные 
    # поля до их родительских значений, чтобы была возможность
    # корректно повторить процесс обновления параметров. 
    # В переменную-буфер копируем получившийся конфиг.
    # Сбрасываем конфиг до состояния входных значений через imtbl_config
    def get_config(self) -> dict:
        buffer = deepcopy(self._config)
        self._config = deepcopy(self._imtbl_config)
        self._recursion_funcs = self._service_funcs
        self._prev_dict = self._config
        return buffer
    
    # При обновление параметров сервиса данный метод перебирает
    # параметры и привязанные к ним функции бизнес логики.
    # Данный метод также реализует рекурсию, если в конфигурации
    # присутствуют вложенности бизнес-логики любого уровня. Принцип простой -
    # если текущий элемент словарь, то обновляем вспомогательные переменные
    # и повторяем процесс для текущего словаря и так далее.
    # Если декоратор в результате вернул None, а не функцию бизнес-логики, 
    # то игнорируем эту функцию, так как для нее не был передан необходимый параметр 
    def _update_config(self, **kwargs) -> None:
        for param, logic_func in self._recursion_funcs.items():
            if param not in self._prev_dict:
                raise ConfigError(f'"{param}" of "{self.name}"')
            
            if isinstance(logic_func, dict):
                self._recursion_funcs = logic_func
                self._prev_dict = self._prev_dict[param]
                return self._update_config(**kwargs)
            else:
                result = logic_func(**kwargs)
                if result is None: continue
                self._prev_dict[param] = result