class StatusMsg():
    OK = 'ok'
    FAIL = 'fail'

class ErrorMsg():
    DB_ERROR = 'db_error'
    VALUES_REQUIRED = 'all_values_are_required'
    MISSING_VALUES = 'missing_values'
    WRONG_PASSWORD = 'wrong_password'
    ROUTE_ERROR = 'endpoint_error'
    NEEDED_VALUES = '[{}] needed value(s)'
    UNKNOWN_ERROR = 'unknown_error'
    AUTH_ERROR = 'authorization_error'
    INVALID_VALUE = 'invalid_value'
    TYPE_ERROR = 'invalid_type'