import contextvars
from typing import Any

aio_databases = contextvars.ContextVar('databases')
redis_var: contextvars.ContextVar[Any] = contextvars.ContextVar('redis')
