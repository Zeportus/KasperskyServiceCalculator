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

services_logic1 = {
    'service_1': {
        'enabled': service2_enabled,
        'nodes': service2_nodes,
        'cpu_cores': service2_cpu_cores,
        'memory': service2_memory
    },

    'service_2': {
        'enabled': service1_enabled,
        'nodes': service1_nodes,
        'memory': service1_memory,
    }
}

error_service_param = {
    'service_1': {
        'enabled': service1_enabled,
    }, 

    'service_2': {
        'enabled': service2_enabled,
        'nodes': service2_nodes,
        'cpu_cores': service2_cpu_cores,
        'memory': service2_memory,
        'unknown': service1_cpu_cores
    }
}

error_service_name = {
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
    },

    'service_3': {
        'enabled': service2_enabled,
        'nodes': service2_nodes,
        'cpu_cores': service2_cpu_cores,
        'memory': service2_memory
    }
}