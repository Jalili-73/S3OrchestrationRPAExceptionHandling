"""Database client."""
from loguru import logger
import psycopg2


class Database:
    """PostgreSQL Database class."""

    def __init__(
            self,
            DATABASE_HOST,
            DATABASE_USERNAME,
            DATABASE_PASSWORD,
            DATABASE_PORT,
            DATABASE_NAME
    ):
        self.host = DATABASE_HOST
        self.username = DATABASE_USERNAME
        self.password = DATABASE_PASSWORD
        self.port = DATABASE_PORT
        self.dbname = DATABASE_NAME
        self.conn = None

    def connect(self):
        """Connect to a Postgres database."""
        if self.conn is None:
            try:
                self.conn = psycopg2.connect(
                    host=self.host,
                    user=self.username,
                    password=self.password,
                    port=self.port,
                    dbname=self.dbname
                )
            except psycopg2.DatabaseError as e:
                LOGGER.error(e)
                raise e
            finally:
                LOGGER.info('Connection opened successfully.')

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def insert_exception(self, robot_id, exception_type, message, resault):
        query = "INSERT INTO public.\"Exception\" (robotid, exception_type, message, resault) " \
                "VALUES (%s, %s, %s, %s)"
        values = (robot_id, exception_type, message, resault)
        self.cursor.execute(query, values)
        self.connection.commit()

    def insert_exception_handler(self, response_time, successability, availability, reliability):
        query = "INSERT INTO public.\"Exception_handler\" " \
                "(response_time, successability, availability, reliability) " \
                "VALUES (%s, %s, %s, %s)"
        values = (response_time, successability, availability, reliability)
        self.cursor.execute(query, values)
        self.connection.commit()

    def insert_resault(self, handler_id, exception_id, handler_start_time, handler_finish_time, handler_success):
        query = "INSERT INTO public.\"Resault\" " \
                "(handler_id, \"exception_Id\", handler_start_time, handler_finish_time, handler_success) " \
                "VALUES (%s, %s, %s, %s, %s)"
        values = (handler_id, exception_id, handler_start_time, handler_finish_time, handler_success)
        self.cursor.execute(query, values)
        self.connection.commit()

    def select_from_exception(self):
        query = "SELECT * FROM public.\"Exception\""
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def select_from_exception_handler(self):
        query = "SELECT * FROM public.\"Exception_handler\""
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def select_from_resault(self):
        query = "SELECT * FROM public.\"Resault\""
        self.cursor.execute(query)
        return self.cursor.fetchall()