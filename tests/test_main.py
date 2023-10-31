import sys
import pytest
sys.path.append(sys.path[0][:-6])
from src.calculator import Calculator, ConfigError
from example_logic import services_logic, services_logic1, error_service_param, error_service_name


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

@pytest.fixture
def calculator():
    only_params = ['disk_storage_MB', 'traffic_mb']
    return Calculator(config, services_logic, only_params)

def test_service_creation(calculator: Calculator):
    assert isinstance(calculator, Calculator)
    assert len(calculator.services) == 2

# Функция принимает получившийся конфиг и словарь верных значений, после чего
# сверяет. Также проверяет, что дополнительные поля у получившегося конфига
# остались без изменений
def check_params_values(updated_config, correct_values: dict):
    exclude_service2_keys = ('add_field', 'in_field', 'another')
    assert isinstance(updated_config, dict)
    assert len(updated_config) == 2
    assert updated_config["service_1"]["nodes"] == correct_values['nodes1']
    assert updated_config["service_2"]["nodes"] == correct_values['nodes2']
    assert updated_config['service_1']['cpu_cores'] == correct_values['cpu_cores1']
    assert updated_config['service_2']['cpu_cores'] == correct_values['cpu_cores2']
    assert updated_config['service_1']['enabled'] == correct_values['enabled1']
    assert updated_config['service_2']['enabled'] == correct_values['enabled2']
    assert updated_config['service_1']['memory'] == correct_values['memory1']
    assert updated_config['service_2']['memory'] == correct_values['memory2']
    # Проверяем, что дополнительные поля не изменились
    for key in exclude_service2_keys:
        assert updated_config['service_2'][key] == config["service_2"][key]

# Передается объект калькулятора с обязательными и необязательными параметрами
# также передаются значения входных параметрво и, соответственно, 
# ожидаемые значения. Передаем три раза одно и то же, меняе только входные
# параметры, это для надежности. Дальше проверяем корректно ли себя
# ведет сервис при передаче параметров без only_params, а также с разным
# количеством самих параметров
@pytest.mark.parametrize(
    'calculator, params, correct_values', 
    [
        (Calculator(config, services_logic, ['disk_storage_MB', 'traffic_mb']),
        {'disk_storage_MB': 1_048_576, 'traffic_mb': 268_435_456},
        {'nodes1': 105, 'nodes2': 2, 'cpu_cores1': 5, 'cpu_cores2': 336,
        'enabled1': True, 'enabled2': True, 'memory1': 105, 'memory2': 100}),

        (Calculator(config, services_logic, ['disk_storage_MB', 'traffic_mb']), 
         {'disk_storage_MB': 1000, 'traffic_mb': 3},
         {'nodes1': 1, 'nodes2': 1, 'cpu_cores1': 5, 'cpu_cores2': 1,
        'enabled1': True, 'enabled2': True, 'memory1': 1, 'memory2': 100}),

        (Calculator(config, services_logic, ['disk_storage_MB', 'traffic_mb']), 
         {'disk_storage_MB': 23_000_000, 'traffic_mb': -400},
         {'nodes1': 2300, 'nodes2': 2, 'cpu_cores1': 5, 'cpu_cores2': 0,
        'enabled1': False, 'enabled2': True, 'memory1': 2300, 'memory2': 100}),

        (Calculator(config, services_logic),
        {'disk_storage_MB': 1_048_576, 'traffic_mb': 268_435_456},
        {'nodes1': 105, 'nodes2': 2, 'cpu_cores1': 5, 'cpu_cores2': 336,
        'enabled1': True, 'enabled2': True, 'memory1': 105, 'memory2': 100}),

        (Calculator(config, services_logic),
        {'disk_storage_MB': 1_048_576},
        {'nodes1': 105, 'nodes2': 2, 'cpu_cores1': 5, 'cpu_cores2': config['service_2']['cpu_cores'],
        'enabled1': config['service_1']['enabled'], 'enabled2': True, 'memory1': 105, 'memory2': 100}),

        (Calculator(config, services_logic),
        {'traffic_mb': 268_435_456},
        {'nodes1': config['service_1']['nodes'], 'nodes2': config['service_2']['nodes'], 'cpu_cores1': 5, 'cpu_cores2': 336,
        'enabled1': True, 'enabled2': config['service_2']['enabled'], 'memory1': config['service_1']['memory'], 'memory2': 100}),

        (Calculator(config, services_logic),
        {},
        {'nodes1': config['service_1']['nodes'], 'nodes2': config['service_2']['nodes'], 'cpu_cores1': 5, 'cpu_cores2': config['service_2']['cpu_cores'],
        'enabled1': config['service_1']['enabled'], 'enabled2': True, 'memory1': config['service_1']['memory'], 'memory2': 100}),
    ]
)
def test_update_config(calculator: Calculator, params, correct_values):
    updated_config = calculator.update_config(**params)
    check_params_values(updated_config, correct_values)

# Здесь обновляются функции бизнес логики. Чтобы понять
# почему именно такие значения - нужно посмотреть как они
# считаются в example_logic.py в разметке services_logic1
@pytest.mark.parametrize(
    'calculator, params, correct_values', 
    [
        (Calculator(config, services_logic, ['disk_storage_MB', 'traffic_mb']),
        {'disk_storage_MB': 1_048_576, 'traffic_mb': 268_435_456},
        {'nodes1': 2, 'nodes2': 105, 'cpu_cores1': 336, 'cpu_cores2': config['service_2']['cpu_cores'],
        'enabled1': True, 'enabled2': True, 'memory1': 100, 'memory2': 105}),

        (Calculator(config, services_logic, ['disk_storage_MB', 'traffic_mb']), 
         {'disk_storage_MB': 1000, 'traffic_mb': 3},
         {'nodes1': 1, 'nodes2': 1, 'cpu_cores1': 1, 'cpu_cores2': config['service_2']['cpu_cores'],
        'enabled1': True, 'enabled2': True, 'memory1': 100, 'memory2': 1}),

        (Calculator(config, services_logic, ['disk_storage_MB', 'traffic_mb']), 
         {'disk_storage_MB': 23_000_000, 'traffic_mb': -400},
         {'nodes1': 2, 'nodes2': 2300, 'cpu_cores1': 0, 'cpu_cores2': config['service_2']['cpu_cores'],
        'enabled1': True, 'enabled2': False, 'memory1': 100, 'memory2': 2300}),

        (Calculator(config, services_logic),
        {'disk_storage_MB': 1_048_576, 'traffic_mb': 268_435_456},
        {'nodes1': 2, 'nodes2': 105, 'cpu_cores1': 336, 'cpu_cores2': config['service_2']['cpu_cores'],
        'enabled1': True, 'enabled2': True, 'memory1': 100, 'memory2': 105}),

        (Calculator(config, services_logic),
        {'disk_storage_MB': 1_048_576},
        {'nodes1': 2, 'nodes2': 105, 'cpu_cores1': config['service_1']['cpu_cores'], 'cpu_cores2': config['service_2']['cpu_cores'],
        'enabled1': True, 'enabled2': True, 'memory1': 100, 'memory2': 105}),

        (Calculator(config, services_logic),
        {'traffic_mb': 268_435_456},
        {'nodes1': config['service_1']['nodes'], 'nodes2': config['service_2']['nodes'], 'cpu_cores1': 336, 'cpu_cores2': config['service_2']['cpu_cores'],
        'enabled1': True, 'enabled2': True, 'memory1': 100, 'memory2': 100}),

        (Calculator(config, services_logic),
        {},
        {'nodes1': config['service_1']['nodes'], 'nodes2': config['service_2']['nodes'], 'cpu_cores1': config['service_1']['cpu_cores'], 'cpu_cores2': config['service_2']['cpu_cores'],
        'enabled1': True, 'enabled2': True, 'memory1': 100, 'memory2': 100}),
    ]
)
def test_update_services_logic(calculator: Calculator, params, correct_values):
    calculator.update_services_logic(services_logic1)
    updated_config = calculator.update_config(**params)
    check_params_values(updated_config, correct_values)
    
def test_config_error_name(calculator: Calculator):
    with pytest.raises(ConfigError):
        calculator.update_services_logic(error_service_name)

def test_config_error_param(calculator: Calculator):
    with pytest.raises(ConfigError):
        calculator.update_services_logic(error_service_param)
        calculator.update_config(disk_storage_MB=1_048_576, traffic_mb=268_435_456)

def test_only_params_error(calculator: Calculator):
    with pytest.raises(Exception):
        calculator.update_config(traffic_mb=268_435_456)
    with pytest.raises(Exception):
        calculator.update_config(disk_storage_MB=1_048_576)
    with pytest.raises(Exception):
        calculator.update_config()
    with pytest.raises(Exception):
        calculator.update_config(left_param='hack', traffic_mb=100)