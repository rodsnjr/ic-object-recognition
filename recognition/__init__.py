from .event import CatalogEvent, CatalogChildEvent

__name__ = 'ic-object-recognition'
__version__ = 0.1

app_name = __name__ + '-' + __version__
broker = 'kafka://localhost'
catalog_topic = 'catalog-topic'
response_topic = 'response-topic'
catalog_dlq = 'catalog-dlq-topic'
