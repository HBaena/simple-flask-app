import multiprocessing

workers = 2
# workers = multiprocessing.cpu_count()*2 + 1   # Or
worker_connections = 1000  # Or more deppending the number or simultaneously clients
# worker_class = 'gevent'
worker_class = 'eventlet'  # testing both for performance
limit_request_line = 0  # 0 to get very large requests
