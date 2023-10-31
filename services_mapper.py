# Здесь просто автоматизируем название конфига в зависимости от сервисов 
# И входных параметров. Это просто пример того, как пользователь сервиса
# может создать свой конфиг и разметить функции-бизнес логики.
# Но так как задача конкретно про эти сервисы, то этот файл также
# является частью решения
import business_logics.kafka as kafka
import business_logics.elastic_search as elastic_search
import business_logics.procesor as procesor
import business_logics.server as server
import business_logics.database_server as database_server
import business_logics.click_house as click_house
import business_logics.synchronizer as synchronizer
import business_logics.scanner as scanner
from copy import deepcopy

services = (kafka, elastic_search, procesor, server, database_server, \
           click_house, synchronizer, scanner)

services_logics = {}
config = {}
config_params = {
    'replicas': 0,
    'memory': 0,
    'cpu': 0,
    'storage': 0
}
for service in services:
    service_funcs = {
        'replicas': service.replicas,
        'memory': service.memory,
        'cpu': service.cpu,
        'storage': service.storage
    }

    service_name = service.__name__.split('.')[1]
    services_logics[service_name] = service_funcs
    config[service_name] = deepcopy(config_params)