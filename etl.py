import configparser
import psycopg2
from sql_queries import *

def load_staging_tables(cur, conn):
    """
    Load data from S3 into Redshift staging tables using COPY commands.
    """
    print("Loading data into staging_events...")
    cur.execute(staging_events_copy)
    conn.commit()

    print("Loading data into staging_songs...")
    cur.execute(staging_songs_copy)
    conn.commit()

    print("Staging tables loaded.")

def insert_tables(cur, conn):
    """
    Transform data from staging tables and insert into star schema tables.
    """
    print("Inserting data into users...")
    cur.execute(user_table_insert)
    conn.commit()

    print("Inserting data into songs...")
    cur.execute(song_table_insert)
    conn.commit()

    print("Inserting data into artists...")
    cur.execute(artist_table_insert)
    conn.commit()

    print("Inserting data into time...")
    cur.execute(time_table_insert)
    conn.commit()

    print("Inserting data into songplays...")
    cur.execute(songplay_table_insert)
    conn.commit()

    print("All data inserted into final tables.")

def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    print("Connecting to Redshift...")
    conn = psycopg2.connect(
        host=config.get("CLUSTER", "HOST"),
        dbname=config.get("CLUSTER", "DB_NAME"),
        user=config.get("CLUSTER", "DB_USER"),
        password=config.get("CLUSTER", "DB_PASSWORD"),
        port=config.get("CLUSTER", "DB_PORT")
    )
    cur = conn.cursor()
    print("Connected.")

    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()
    print("ETL process completed successfully.")

if __name__ == "__main__":
    main()
