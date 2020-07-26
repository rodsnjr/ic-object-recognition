class Resource:
    inception = ''
    inception_labels = ''


class FileConfig:
    def __init__(self, client='s3'):
        self.client = client


class CacheConfig:
    def __init__(self, client='redis'):
        self.client = client
        self.host = None


class DatabaseConfig:
    def __init__(self, user, password,
                 database, host,
                 client):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.client = client

    def get_url(self):
        pass


class Queues:
    def __init__(self, catalog='catalog'):
        self.catalog = catalog


def build_file_config(context) -> FileConfig:
    if context == 'mock':
        return FileConfig(client=context)
    return FileConfig()


def build_cache_config(context) -> CacheConfig:
    if context == 'mock':
        return CacheConfig(client=context)
    return CacheConfig()


def build_db_config(context) -> DatabaseConfig:
    if context == 'mock':
        return DatabaseConfig(client=context)
    return DatabaseConfig()


def build_queues(context) -> Queues:
    if context == 'mock':
        return Queues()
    return Queues()
