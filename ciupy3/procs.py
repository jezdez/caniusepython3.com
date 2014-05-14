from hirefire.procs.rq import RQProc
from redis_cache import get_redis_connection


class WorkerProc(RQProc):
    name = 'worker'
    queues = ['default']
    connection = get_redis_connection()


class HighWorkerProc(RQProc):
    name = 'high-worker'
    queues = ['high']
    connection = get_redis_connection()
