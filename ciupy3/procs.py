from hirefire.procs.rq import RQProc
from redis_cache import get_redis_connection


class WorkerProc(RQProc):
    name = 'worker'
    queues = ['low', 'default', 'high']
    connection = get_redis_connection()
