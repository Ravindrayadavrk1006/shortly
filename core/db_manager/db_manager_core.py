from sqlalchemy import create_engine, Table, MetaData, select, insert, update, delete
from sqlalchemy.exc import SQLAlchemyError
import urllib.parse
import os
from contextlib import contextmanager
from ..loggings.logging_config import logger
class DatabaseManager:
    def __init__(
            self,
            host,
            port,
            password,
            use_ssl = False,
            verify_ssl = False,
            username = 'postgres',
            pool_size = 10,
            max_overflow = 5,
            pool_recycle = 1800
            ):
        self.host = host
        self.port = port
        self.safe_password = urllib.parse.quote_plus(password)
        self.safe_username = urllib.parse.quote_plus(username)
        self.db_name = os.environ.get('DB_NAME')
        self.use_ssl = use_ssl
        self.verify_ssl = verify_ssl
        self.schema = os.environ.get('SCHEMA_NAME')
        self.database = 'postgresql'
        self.db_url = f"{self.database}://{self.safe_username}:{self.safe_password}@{self.host}:{self.port}/{self.db_name}"
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        self.pool_recycle = pool_recycle
        self.table_name = os.environ.get('TABLE_NAME')
        #create the engine
        self.engine = self.__create_engine()
        #load the table in orm format
        self._get_db()

    def _get_db(self):
        self.metadata = MetaData()
        self.url_table = Table('url_shortner_tb',self.metadata, schema= self.schema, autoload_with= self.engine)

    def __create_engine(self):
        engine = create_engine(
            self.db_url,
            pool_size = self.pool_size,
            max_overflow= self.max_overflow,
            pool_recycle= self.pool_recycle)
        
        return engine

    @contextmanager
    def get_engine_session(self):
        conn = self.engine.connect()

        #begin a transaction
        transaction = conn.begin()
        try:
            yield conn
            transaction.commit()
        except Exception as e:
            transaction.rollback()
            logger.exception(f'error raised while executing a db query {e}')
            raise
        finally:
            conn.close()
    

    def get_all_rows(self):
        try:
            query = select(self.url_table).order_by(self.url_table.c.created_at.desc())

            with self.get_engine_session() as connection:
                result = connection.execute(query)
                data = result.fetchall()
            return data
        except Exception as e:
            raise
    

    def insert_into_table(self, short_hash, long_url, url_counter):
        try:
            query = insert(self.url_table).values(
                short_hash = short_hash,
                long_url = long_url,
                url_counter = url_counter
            )
            with self.get_engine_session() as conn:
                result = conn.execute(query)
                logger.info(result)
            return short_hash
        except SQLAlchemyError as e:
            raise
    

    def get_long_url(self, short_hash):
        try:
            query = select(self.url_table).where(self.url_table.c.short_hash == short_hash).order_by(self.url_table.c.created_at.desc())

            with self.get_engine_session() as conn:
                result = conn.execute(query)
                data = result.fetchone()
            return data

           
        except SQLAlchemyError as e:
            raise