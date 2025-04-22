# sql_queries.py

import configparser

# Load config
config = configparser.ConfigParser()
config.read('dwh.cfg')

# S3 & IAM configs
LOG_DATA = config.get('S3', 'LOG_DATA')
LOG_JSONPATH = config.get('S3', 'LOG_JSONPATH')
SONG_DATA = config.get('S3', 'SONG_DATA')
IAM_ROLE = config.get('IAM_ROLE', 'ARN')

# DROP TABLES
staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES
staging_events_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_events (
    artist TEXT,
    auth TEXT,
    firstName TEXT,
    gender CHAR(1),
    itemInSession INT,
    lastName TEXT,
    length FLOAT,
    level TEXT,
    location TEXT,
    method TEXT,
    page TEXT,
    registration BIGINT,
    sessionId INT,
    song TEXT,
    status INT,
    ts BIGINT,
    userAgent TEXT,
    userId INT
);
""")

staging_songs_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_songs (
    num_songs INT,
    artist_id TEXT,
    artist_latitude FLOAT,
    artist_longitude FLOAT,
    artist_location TEXT,
    artist_name TEXT,
    song_id TEXT,
    title TEXT,
    duration FLOAT,
    year INT
);
""")

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (
    songplay_id INT IDENTITY(0,1) PRIMARY KEY,
    start_time TIMESTAMP NOT NULL,
    user_id INT NOT NULL,
    level TEXT,
    song_id TEXT,
    artist_id TEXT,
    session_id INT,
    location TEXT,
    user_agent TEXT
);
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    gender CHAR(1),
    level TEXT
);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (
    song_id TEXT PRIMARY KEY,
    title TEXT,
    artist_id TEXT,
    year INT,
    duration FLOAT
);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (
    artist_id TEXT PRIMARY KEY,
    name TEXT,
    location TEXT,
    latitude FLOAT,
    longitude FLOAT
);
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time (
    start_time TIMESTAMP PRIMARY KEY,
    hour INT,
    day INT,
    week INT,
    month INT,
    year INT,
    weekday INT
);
""")

# COPY INTO STAGING TABLES
staging_events_copy = f"""
COPY staging_events
FROM '{LOG_DATA}'
IAM_ROLE '{IAM_ROLE}'
JSON '{LOG_JSONPATH}'
REGION 'us-west-2';
"""

staging_songs_copy = f"""
COPY staging_songs
FROM '{SONG_DATA}'
IAM_ROLE '{IAM_ROLE}'
JSON 'auto'
REGION 'us-west-2';
"""

# INSERT INTO FINAL TABLES
songplay_table_insert = ("""
INSERT INTO songplays (
    start_time, user_id, level, song_id, artist_id, session_id, location, user_agent
)
SELECT DISTINCT
    TIMESTAMP 'epoch' + se.ts/1000 * INTERVAL '1 second' AS start_time,
    se.userId,
    se.level,
    ss.song_id,
    ss.artist_id,
    se.sessionId,
    se.location,
    se.userAgent
FROM staging_events se
JOIN
