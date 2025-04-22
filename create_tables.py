import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries

def create_database():
    """
    - Reads config file
    - Connects to Redshift cluster
    - Returns cursor and connection
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect(
        host=config.get("CLUSTER", "HOST"),
        dbname=config.get("CLUSTER", "DB_NAME"),
        user=config.get("CLUSTER", "DB_USER"),
        password=config.get("CLUSTER", "DB_PASSWORD"),
        port=config.get("CLUSTER", "DB_PORT")
    )
    cur = conn.cursor()
    return cur, conn

def drop_tables(cur, conn):
    """
    Executes all DROP TABLE statements from sql_queries
    """
    for query in drop_table_queries:
        print(f"Running DROP TABLE: {query[:40]}...")
        cur.execute(query)
        conn.commit()

def create_tables(cur, conn):
    """
    Executes all CREATE TABLE statements from sql_queries
    """
    for query in create_table_queries:
        print(f"Running CREATE TABLE: {query[:40]}...")
        cur.execute(query)
        conn.commit()

def main():
    """
    - Connects to Redshift
    - Drops old tables
    - Creates new tables
    - Closes connection
    """
    cur, conn = create_database()

    print("Dropping tables if they exist...")
    drop_tables(cur, conn)

    print("Creating tables...")
    create_tables(cur, conn)

    conn.close()
    print("All tables created successfully!")

if __name__ == "__main__":
    main()
