import sqlite3
from sqlite3 import Error
import os


def check_dir_exists():
    # checking if the directory C:\sqlite\db exist or not.
    if not os.path.exists("C:\sqlite\db"):

        # if the C:\sqlite\db\ directory is not present
        # then create it.
        os.makedirs("C:\sqlite\db")


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    check_dir_exists()
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    check_dir_exists()
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_result(conn, result):
    """ create a new result
    :param conn: Connection object
    :param result
    :return:
    """
    sql = ''' INSERT INTO results(name,score)
              VALUES(?,?)'''
    cur = conn.cursor()
    cur.execute(sql, result)
    conn.commit()


def CreateTableResults():
    conn = create_connection(r"C:\sqlite\db\pythonsqlite.db")
    sql_create_results_table = """CREATE TABLE IF NOT EXISTS results (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    score integer
                                );"""
    # create table
    if conn is not None:
        # create results table
        create_table(conn, sql_create_results_table)
    else:
        print("Error! Cannot create the database connection.")


def AddResult(name, score):
    conn = create_connection(r"C:\sqlite\db\pythonsqlite.db")
    with conn:
        result = (name, score)
        create_result(conn, result)


def leader_board():
    conn = create_connection(r"C:\sqlite\db\pythonsqlite.db")
    with conn:
        cur = conn.cursor()
        cur.execute('SELECT *FROM results ORDER BY score desc LIMIT 10')
        rows = cur.fetchall()
        return rows
