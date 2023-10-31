from src.calculator import used_parameters
import math


@used_parameters('agents', 'distributed')
def replicas(agents: int, distributed: bool):
    if agents > 0:
        if distributed:
            res = agents / 15000
            res = float(f'{res:.1f}')
            return max(res, 1)
        else: return 1
    return 0

@used_parameters('distributed', 'storage')
def memory(distributed: bool, storage: float):
    if distributed: return float(f'{(storage*1.6):.3f}')
    return 100

@used_parameters()
def cpu(): return 1

@used_parameters('agents', 'nodes')
def storage(agents: int, nodes: int):
    if nodes > 0: 
        res = (0.00000002*agents*agents+0.00067749*agents+4.5)*agents/nodes
        return math.ceil(res * 1000) / 1000
    return 0
