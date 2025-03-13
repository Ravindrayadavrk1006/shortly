from sqlalchemy import create_engine, Table, MetaData, select, insert, update, delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import urllib.parse
import os
from contextlib import contextmanager
from ..loggings.logging_config import logger
class DatabaseManager:
    #declare a static variable for getting the db_engine
    _engine = None
    _db_tables = None
    _schema = None
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
        if not DatabaseManager._schema:
            DatabaseManager._schema = os.environ.get('SCHEMA_NAME')
        self.schema = DatabaseManager._schema
        self.database = 'postgresql'
        self.db_url = f"{self.database}://{self.safe_username}:{self.safe_password}@{self.host}:{self.port}/{self.db_name}"
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        self.pool_recycle = pool_recycle
        self.table_name = os.environ.get('TABLE_NAME')
        #create the engine, in singleton design pattern
        if not DatabaseManager._engine:
            DatabaseManager._engine = self.__create_engine()
        self.engine = DatabaseManager._engine
        if  DatabaseManager._db_tables is None:
            DatabaseManager._db_tables = self._get_tables()
        self.url_table = DatabaseManager._db_tables

        #load the table in orm format
        self.SessionLocal = sessionmaker(bind=self.engine)

    @staticmethod
    def _get_tables():
        metadata = MetaData()
        url_table = Table('url_shortner_tb',metadata, schema= DatabaseManager._schema, autoload_with= DatabaseManager._engine)
        return url_table

    def __create_engine(self):
        engine = create_engine(
            self.db_url,
            pool_size = self.pool_size,
            max_overflow= self.max_overflow,
            pool_recycle= self.pool_recycle)
        
        return engine

    @contextmanager
    def get_engine_session(self):
        session = self.SessionLocal()  # Get a session from the session factory
        try:
            yield session
            session.commit()  # Commit transaction if everything is fine
        except Exception as e:
            session.rollback()  # Rollback on error
            logger.exception(f"Error raised while executing a DB query: {e}")
            raise
        finally:
            session.close()  # Always close the session
    

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