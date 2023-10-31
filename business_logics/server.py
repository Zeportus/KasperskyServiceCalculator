from src.calculator import used_parameters
import math


@used_parameters('agents', 'storage')
def replicas(agents: int, storage: float):
    if agents > 0 and storage > 0:
        return min(agents, 2)
    return 0

@used_parameters('distributed', 'traffic')
def memory(distributed: bool, traffic: float):
    if distributed: return float(f'{(traffic*0.5):.3f}')
    return 100

@used_parameters()
def cpu(): return 1

@used_parameters('agents', 'nodes')
def storage(agents: int, nodes: int):
    if nodes > 0:
        res = 0.0019 * agents + 2.3154
        return math.ceil(res * 1000) / 1000
    return 0     
