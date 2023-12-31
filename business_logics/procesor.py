from src.calculator import used_parameters
import math


@used_parameters('distributed', 'agents', 'storage')
def replicas(distributed: bool, agents: int, storage: float):
    if agents > 0 and storage > 0:
        return 3 if distributed else 0
    return 0

@used_parameters('distributed', 'traffic')
def memory(distributed: bool, traffic: float):
    if distributed: return traffic * 0.5
    return 100

@used_parameters()
def cpu(): return 3

@used_parameters('agents', 'nodes')
def storage(agents: int, nodes: int):
    if nodes > 0:
        res = -4.25877 + 0.98271 * math.log1p(agents)
        return math.ceil(res * 1000) / 1000
    return 0
    
     
