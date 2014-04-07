from hirefire.procs.pq import PQProc


class WorkerProc(PQProc):
    name = 'worker'
    queues = ['default']
