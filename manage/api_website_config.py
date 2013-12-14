from ukutil import is_in_unittest

FRONTEND_PORT = 4999
API_PORT = 5000

API_RUN_OPTIONS = {
    'debug': True,
    'use_reloader': not is_in_unittest()
}

FRONTEND_RUN_OPTIONS = {
    'debug': True
}
