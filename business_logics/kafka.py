from src.calculator import used_parameters
import math


@used_parameters('distributed')
def replicas(distributed: bool):
    return 3 if distributed else 1

@used_parameters('distributed', 'mail_traffic')
def memory(distributed: bool, mail_traffic: float):
    return mail_traffic * 0.5 if distributed else 100

@used_parameters('agents', 'nodes')
def cpu(agents: int, nodes: int):
    res = (0.000169*agents+0.437923)*nodes/3
    return math.ceil(res * 100) / 100

@used_parameters('agents')
def storage(agents: int):
    res = 0.0004*agents+0.3231
    return math.ceil(res * 1000) / 1000   
