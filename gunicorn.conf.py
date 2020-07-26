# default is 30 seconds
timeout = 60
worker_class = 'gevent'
loglevel = 'info'  # default is info
accesslog = '-'  # output to sdtout
access_log_format = ('%(h)s %(l)s %(u)s %(t)s "%(r)s" '
                     '%(s)s %(b)s "%(f)s" "%(a)s" '
                     'user_id=%({x-es-user}o)s %(l)s '
                     'request_id=%({x-es-request}o)s %(l)s ')
