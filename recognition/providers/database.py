from tortoise import Tortoise
from .config import DatabaseConfig

_ABSTRACT_METHOD = 'Abstract Method'


class DatabaseClient:
    def __init__(self, database_config: DatabaseConfig):
        self.database_config = database_config

    async def get_modules(self) -> dict:
        raise NotImplementedError(_ABSTRACT_METHOD)

    async def connect(self):
        raise NotImplementedError(_ABSTRACT_METHOD)


class MockDatabaseClient(DatabaseClient):
    async def get_modules(self) -> dict:
        pass

    async def connect(self):
        pass


class PostgresClient(DatabaseClient):
    def get_modules(self) -> dict:
        return dict()

    def connect(self):
        await Tortoise.init(
            db_url=self.database_config.get_url(),
            modules=self.get_modules()
        )
        # Generate the schema
        await Tortoise.generate_schemas()
