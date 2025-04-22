import asyncpg
from os import environ

host = environ.get("POSTGRES_HOST", "localhost")
user = environ.get("POSTGRES_USER", "o2p")
db = environ.get("POSTGRES_DB", "o2p")

DATABASE_URL = f"postgresql://{user}@{host}/{db}"

# print(DATABASE_URL)

class Postgres:
    def __init__(self, database_url: str):
        self.database_url = database_url

    async def connect(self):
        self.pool = await asyncpg.create_pool(self.database_url)

    async def disconnect(self):
        await self.pool.close()

database = Postgres(DATABASE_URL)