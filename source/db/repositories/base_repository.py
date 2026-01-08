from asyncpg import Connection


class BaseRepository:
    def __init__(self, connection: Connection):
        self.connection = connection
