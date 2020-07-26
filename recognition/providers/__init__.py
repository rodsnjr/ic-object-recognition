from .config import Resource

from os import environ
from .provider import Provider, ConfigProvider

_CONTEXT = 'APPLICATION_CONTEXT'
_DEFAULT_CONTEXT = 'mock'
_APP_CONTEXT = environ.get(_CONTEXT, _DEFAULT_CONTEXT)

_config = ConfigProvider(_APP_CONTEXT)
_provider = Provider(_config)

file_client = _provider.file_client()
cache_client = _provider.cache_client()
queues = _config.queues

__all__ = [
    file_client,
    cache_client,
    queues
]
