# 🎵 Sparkify Data Warehouse on AWS Redshift

This project builds a cloud-based data warehouse for Sparkify, a music streaming startup. The goal is to analyze user behavior and song play data using AWS infrastructure, enabling efficient analytics through star-schema design and distributed query execution.

---

## 🗂️ Project Structure


```bash
Sparkify_data_warehouse_aws/
├── sql_queries.py                # create sql_queries
│ 
├── create_tables.py              # connections with redshift cluster and create tables
├── etl                           # ETL process pipeline
├── test queries                  # Data valorisation
└── README.md              # This file

``` 


---

## 🎧 Dataset

### Source
Data is collected from two S3 buckets:

- **Song data**: `s3://sparkify-project-aws/song_data/`
- **Log data**: `s3://sparkify-project-aws/log_data/`  
  (log format inspired by Udacity’s public dataset)

### JSON format example (log_data):
```json
{
  "artist": "Muse",
  "auth": "Logged In",
  "firstName": "Ryan",
  "gender": "M",
  "itemInSession": 0,
  "lastName": "Smith",
  "length": 210.123,
  "level": "free",
  "location": "Dallas, TX",
  "method": "PUT",
  "page": "NextSong",
  "registration": 1540990648796,
  "sessionId": 902,
  "song": "Uprising",
  "status": 200,
  "ts": 1541106106796,
  "userAgent": "\"Mozilla/5.0\"",
  "userId": "42"
}

 ``` 

## 🏗️ Data Warehouse Design

### Star Schema
Fact Table: songplays

Dimension Tables: users, songs, artists, time

### ETL Process
Load raw JSON data from S3 into staging tables via Redshift COPY

Transform data using SQL joins and timestamp parsing

Insert into final fact and dimension tables

## 🛠️ Pipeline Execution
Setup Redshift cluster and IAM Role

Upload log_json_path.json to S3

Update dwh.cfg with cluster, role, and S3 paths

Run:

```  bash

python create_tables.py
python etl.py
``` 

## 🧩 Problem #1: staging_events Loaded but User Columns Are Null
### Issue
staging_events loaded ~8,000 rows, but userId, firstName, etc., were all None.

### Cause
Redshift’s COPY ... JSON 'auto' couldn’t infer mappings from the log structure.

### Solution
Created and uploaded a custom JSONPaths file (log_json_path.json) and updated dwh.cfg:

```  ini

LOG_JSONPATH='s3://sparkify-project-aws/log_json_path.json'
``` 

## problem #2: songplays Table Remained Empty

### Issue
songplays table wasn’t populated, despite valid staging data.

### Cause
The JOIN between staging_events and staging_songs was too strict, requiring:

``` sql
se.song = ss.title AND se.artist = ss.artist_name AND se.length = ss.duration 

```

### Solution
Replaced with a more forgiving LEFT JOIN:

``` sql

ON se.song ILIKE ss.title
AND se.artist ILIKE ss.artist_name
AND ABS(se.length - ss.duration) < 1

``` 
This enabled partial matches and allowed unmatched songplays to still be logged with NULL song/artist IDs.


## Sample Queries
### Top 5 Active Users

```  sql

SELECT user_id, COUNT(*) AS play_count
FROM songplays
GROUP BY user_id
ORDER BY play_count DESC
LIMIT 5;

``` 
### Most Played Songs

```  sql

SELECT s.title, COUNT(*) AS plays
FROM songplays sp
JOIN songs s ON sp.song_id = s.song_id
GROUP BY s.title
ORDER BY plays DESC
LIMIT 5;

``` 

## 🧠 Author
Chetara AbdelOuahab
GitHub: @chetara