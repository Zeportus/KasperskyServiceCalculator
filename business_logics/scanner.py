from src.calculator import used_parameters
import math


@used_parameters('agents')
def replicas(agents: int):
    if agents > 0: return 1
    return 0

@used_parameters()
def memory():
    return 300

@used_parameters()
def cpu(): return 1

@used_parameters('agents', 'distributed')
def storage(agents: int, distributed: bool):
    if distributed:
        res = 0.0002 * agents + 0.6
        return math.ceil(res * 1000) / 1000
    return 0
