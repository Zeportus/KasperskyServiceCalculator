from src.calculator import used_parameters


@used_parameters('distributed')
def replicas(distributed: bool):
    return 3 if distributed else 1

@used_parameters()
def memory(): return 0

@used_parameters()
def cpu(): return 3

@used_parameters('agents')
def storage(agents: int):
    if agents < 5000: return 0.256
    elif agents < 10000: return 0.512
    return 1