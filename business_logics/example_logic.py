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

@used_parameters('disk_storage_MB')
def service1_memory(disk_storage_MB) -> float:
    return math.ceil(disk_storage_MB / 10000)

@used_parameters()
def service2_enabled() -> bool:
    return True

@used_parameters('disk_storage_MB')
def service2_nodes(disk_storage_MB) -> int:
    return 2 if math.ceil(disk_storage_MB / 100000) > 3 else 1

@used_parameters('traffic_mb')
def service2_cpu_cores(traffic_mb) -> int:
    return math.ceil((traffic_mb / 8) / 100000)

@used_parameters()
def service2_memory() -> float:
    return 100

@used_parameters()
def service1_func1():
    print('AOAOA')
    return 1

@used_parameters()
def service1_func2():
    print('BJBJJBJ')
    return 1

services_logic = {
    'service_1': {
        'enabled': service1_enabled,
        'nodes': service1_nodes,
        'cpu_cores': service1_cpu_cores,
        'memory': service1_memory,
        'in': {
            'func1': service1_func1,
            'in1': {
                'func2': service1_func2,
                'in2': {
                    'func3': service1_func1,
                    'func4': service1_func1
                }
            },
            'in2': {
                'func6': service1_func2
            }
        },
        'in1': {
                'in2': {
                    'func5': service1_func2
                }
            }
    },

    'service_2': {
        'enabled': service2_enabled,
        'nodes': service2_nodes,
        'cpu_cores': service2_cpu_cores,
        'memory': service2_memory
    }
}

services_logic1 = {
    'service_1': {
        
    },

    'service_2': {
        'enabled': service2_enabled,
        'nodes': service2_nodes,
        'cpu_cores': service2_cpu_cores,
        'memory': service2_memory
    }
}