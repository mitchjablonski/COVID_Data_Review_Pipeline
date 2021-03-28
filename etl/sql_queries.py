import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

IAM_ROLE = config['IAM_ROLE']['ARN']
LOG_DATA = config['S3']['LOG_DATA']
VAC_TWEETS = config['S3']['VAC_TWEETS']
VAC_RESPONSE = config['S3']['VAC_RESPONSE']
VAC_SYMPTOMS = config['S3']['VAC_SYMPTOMS']
VAC_TYPE = config['S3']['VAC_TYPE']

# DROP TABLES

staging_covid_tweets_drop = "DROP TABLE IF EXISTS staging_covid_tweets"
covid_tweets_drop = "DROP TABLE IF EXISTS covid_tweets"

staging_covid_vaccine_tweets_drop = "DROP TABLE IF EXISTS staging_covid_vaccine_tweets"
covid_vaccine_tweets_drop = "DROP TABLE IF EXISTS covid_vaccine_tweets"

staging_covid_article_data_drop = "DROP TABLE IF EXISTS covid_article_data"
covid_article_data_drop = "DROP TABLE IF EXISTS covid_article_data"


vaccine_data_drop = "DROP TABLE IF EXISTS vaccine_data"
vaccine_response_data_drop = "DROP TABLE IF EXISTS vaccine_response_data"
vaccine_symptom_data_drop = "DROP TABLE IF EXISTS vaccine_symptom_data"

time_table_drop = "DROP TABLE IF EXISTS time_table"

# CREATE TABLES

staging_covid_article_data_create = ("""CREATE TABLE IF NOT EXISTS staging_covid_article_data(
                                cord_uid TEXT,
                                sha TEXT,
                                source_x TEXT,
                                title TEXT,
                                doi TEXT,
                                pmcid TEXT,
                                pubmed_id TEXT,
                                license TEXT,
                                abstract TEXT,
                                publish_time TEXT,
                                authors TEXT,
                                jounal TEXT,
                                mag_id TEXT,
                                who_covidence_id TEXT,
                                arxiv_id TEXT,
                                pdf_json_files TEXT,
                                pmc_json_files TEXT,
                                url TEXT,            
                                s2_id TEXT )
""")

staging_covid_vaccine_tweets_create = ("""CREATE  TABLE IF NOT EXISTS staging_covid_vaccine_tweets(
                                user_name TEXT,
                                user_location TEXT,
                                user_description NUMERIC,
                                user_created NUMERIC,
                                user_friends TEXT,
                                user_favourites TEXT,
                                user_verified TEXT,
                                date TEXT,
                                text TEXT,
                                hashtags TEXT,
                                source TEXT,
                                is_retweet BOOL)
""")

staging_covid_tweets_create = ("""CREATE  TABLE IF NOT EXISTS staging_covid_tweets(
                                user_name TEXT,
                                user_location TEXT,
                                user_description NUMERIC,
                                user_created NUMERIC,
                                user_friends TEXT,
                                user_favourites TEXT,
                                user_verified TEXT,
                                date TEXT,
                                text TEXT,
                                hashtags TEXT,
                                source TEXT,
                                is_retweet BOOL)
""")


covid_vaccine_tweets_create = ("""CREATE  TABLE IF NOT EXISTS staging_covid_vaccine_tweets(
                                id SERIAL PRIMARY KEY,
                                user_name TEXT,
                                user_location TEXT,
                                date TEXT,
                                text TEXT)
""")

covid_tweets_create = ("""CREATE  TABLE IF NOT EXISTS covid_tweets(
                                id SERIAL PRIMARY KEY,
                                user_name TEXT,
                                user_location TEXT,
                                date TEXT,
                                text TEXT)
""")

covid_tweets_create = ("""CREATE  TABLE IF NOT EXISTS covid_vaccine_tweets(
                                id SERIAL PRIMARY KEY,
                                user_name TEXT,
                                user_location TEXT,
                                date TEXT,
                                text TEXT)
""")


covid_article_data_create = ("""CREATE TABLE IF NOT EXISTS staging_covid_article_data(
                                cord_uid TEXT PRIMARY KEY,
                                title TEXT,
                                abstract TEXT,
                                publish_time TEXT,
                                authors TEXT)
""")


vaccine_data_create = ("""CREATE TABLE IF NOT EXISTS vaccine_data(
                                VAERS_ID TEXT PRIMARY KEY,
                                RECVDATE TEXT,
                                AGE_YRS FLOAT,
                                CAGE_YR FLOAT,
                                CAGE_MO TEXT,
                                SEX TEXT,
                                RPT_DATE TEXT,
                                SYMPTOM_TEXT TEXT,
                                DIED TEXT,
                                DATEDIED TEXT,
                                L_THREAT TEXT,
                                ER_VISI TEXT,
                                HOSPITAL TEXT,
                                HOSPDAYS TEXT,
                                X_STAY TEXT,
                                DISABLE TEXT,
                                RECOVD TEXT,
                                VAX_DAT TEXT,
                                ONSET_DATE TEXT,
                                NUMDAYS TEXT,
                                LAB_DATA TEXT,
                                V_ADMINBY TEXT,
                                V_FUNDB TEXT,
                                OTHER_MEDS TEXT,
                                CUR_ILL TEXT,
                                HISTORY TEXT,
                                PRIOR_VAX TEXT,
                                SPLTTYP TEXT,
                                FORM_VERS TEXT,
                                TODAYS_DATE TEXT,
                                BIRTH_DEFECT TEXT,
                                OFC_VISIT TEXT,
                                ER_ED_VISI TEXT,
                                ALLERGIES TEXT)
""")


vaccine_response_data_create = ("""CREATE TABLE IF NOT EXISTS vaccine_response_data(
                                VAERS_ID TEXT PRIMARY KEY,
                                SYMPTOM1 TEXT,
                                SYMPTOMVERSION1 FLOAT,
                                SYMPTOM2 TEXT,
                                SYMPTOMVERSION2 FLOAT,
                                SYMPTOM3 TEXT,
                                SYMPTOMVERSION3 FLOAT,
                                SYMPTOM4 TEXT,
                                SYMPTOMVERSION4 FLOAT,
                                SYMPTOM5 TEXT,
                                SYMPTOMVERSION5 FLOAT)
""")

vaccine_response_data_create = ("""CREATE TABLE IF NOT EXISTS vaccine_response_data(
                                VAERS_ID TEXT PRIMARY KEY,
                                VAX_TYPE TEXT,
                                VAX_MANU TEXT,
                                VAX_LOT TEXT,
                                VAX_DOSE_SERIES TEXT,
                                VAX_ROUTE TEXT,
                                VAX_SITE TEXT,
                                VAX_NAME TEXT)
""")

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplay(
                            songplay_id INT IDENTITY(0,1) PRIMARY KEY,
                            start_time TIMESTAMP NOT NULL,
                            user_id INTEGER NOT NULL,
                            level TEXT,
                            song_id TEXT,
                            artist_id TEXT,
                            session_id INTEGER,
                            location TEXT,
                            user_agent TEXT)
""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS users(
                        user_id INTEGER PRIMARY KEY,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL,
                        gender TEXT,
                        level TEXT)
""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS songs(
                        song_id TEXT PRIMARY KEY,
                        title TEXT,
                        artist_id TEXT,
                        year INTEGER,
                        duration NUMERIC)
""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artist(
                          artist_id TEXT PRIMARY KEY,
                          name TEXT,
                          location TEXT,
                          latitude NUMERIC,
                          longitude NUMERIC)
""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time(
                        start_time TIMESTAMP PRIMARY KEY,
                        hour INTEGER,
                        day INTEGER,
                        week INTEGER,
                        month INTEGER,
                        year INTEGER,
                        weekDay INTEGER)
""")

# POPULATE STAGING TABLES

staging_events_copy = (f"""copy staging_events from {LOG_DATA}
                          credentials 'aws_iam_role={IAM_ROLE}'
                          DELIMITER ','
                          CSV HEADER""")

staging_songs_copy = (f"""copy staging_songs from {SONG_DATA} 
                          credentials 'aws_iam_role={IAM_ROLE}'
                          json 'auto'
                          """)


# POPULATE FINAL TABLES
songplay_table_insert = ("""INSERT INTO songplay(start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
                            SELECT timestamp 'epoch' + ts * interval '1 second' AS start_time, user_id, level, song_id, artist_id, session_id, location, user_agent
                            FROM staging_events se
                            JOIN staging_songs ss ON ((se.artist = ss.artist_name) and (se.song = ss.title) and (se.length=ss.duration))
                            WHERE se.page = 'NextSong'
""")

user_table_insert = ("""INSERT INTO users(user_id, first_name, last_name, gender, level)
                        SELECT DISTINCT user_id, first_name, last_name, gender, level
                        FROM staging_events
                        WHERE user_id IS NOT NULL and
                        page = 'NextSong'
""")

song_table_insert = ("""INSERT INTO songs(song_id, title, artist_id, year, duration)
                        SELECT song_id, title, artist_id, year, duration
                        FROM staging_songs
                        WHERE song_id IS NOT NULL
""")

artist_table_insert = ("""INSERT INTO artist(artist_id, name, location, latitude, longitude)
                          SELECT artist_id, artist_name as name, artist_location as location, artist_latitude as latitude, artist_longitude as longitude
                          FROM staging_songs
                          WHERE artist_id IS NOT NULL
""")

time_table_insert = ("""INSERT INTO time(start_time, hour, day, week, month, year, weekDay)
                        SELECT timestamp 'epoch' + ts * interval '1 second' AS start_time, extract(hour from start_time), 
                        extract(day from start_time), extract(week from start_time), extract(month from start_time), 
                        extract(year from start_time), extract(dayofweek from start_time)
                        FROM staging_events
                        WHERE start_time IS NOT NULL and
                        page = 'NextSong'
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]