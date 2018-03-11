from sqlalchemy import create_engine, MetaData, Integer, Table, Column, Boolean
import os
import psycopg2
import logging


def db_define(env):
    """ This function defines the database schema

    Args:
        env: database connection object
    """
    logger.info('sqlalchemy create_engine')
    engine = create_engine(env)
    meta = MetaData(bind=engine)

    logger.info('Define table')
    Table('results_cache', meta,
          Column('request_time', Long, primary_key=True,
                 autoincrement=True),
          Column('station_id', Integer, primary_key=False, autoincrement=False),
          Column('percent_full', Float, nullable=True),
          Column('result', Float, nullable=True)
          )

    logger.info('Call create_all()')
    meta.create_all()


def post_result(request_time, station_id, percent_full, result):
    # set up connection
    connection = pymysql.connect(
            dbname=os.getenv("DATABASE"),
            user=os.getenv("DB_USERNAME"),
            password=os.getenv("PASSWORD"),
            host=os.getenv("HOST")
            )
    cur = connection.cursor()

    # write result into database
    cur.execute("INSERT INTO results_cache (request_time, station_id, percent_full, result) \
    VALUES (%s,%s,%s)", (request_time, station_id, percent_full, result))
        # commit and close database connection
    connection.commit()
    connection.close()


if __name__ == "__main__":
    # set up logging
    log_fmt = '%(asctime)s -  %(levelname)s - %(message)s'
    logging.basicConfig(filename='create_db.log', level=logging.INFO,
                        format=log_fmt)
    logger = logging.getLogger(__name__)

    # set up database and connection
    logger.info('Get database url from environment')
    db = db_define(os.environ.get("DATABASE_URL"))

    logger.info('Set up database connection')
    connection = pymysql.connect(
      dbname=os.getenv("DATABASE"),
      user=os.getenv("DB_USERNAME"),
      password=os.getenv("PASSWORD"),
      host=os.getenv("HOST")
      )
    cur = connection.cursor()