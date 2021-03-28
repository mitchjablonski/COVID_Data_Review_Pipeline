import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

IAM_ROLE = config['IAM_ROLE']['ARN']
COVID_TWEETS = config['S3']['COVID_TWEETS']
VAC_TWEETS = config['S3']['VAC_TWEETS']
VAC_RESPONSE = config['S3']['VAC_RESPONSE']
VAC_SYMPTOMS = config['S3']['VAC_SYMPTOMS']
VAC_TYPE = config['S3']['VAC_TYPE']
ARTICLE_DATA = config['S3']['ARTICLE_DATA']

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
                                is_retweet BOOLEAN)
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

covid_vaccine_tweets_create = ("""CREATE  TABLE IF NOT EXISTS covid_vaccine_tweets(
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

covid_article_data_create = ("""CREATE TABLE IF NOT EXISTS covid_article_data(
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

vaccine_symptom_data_create = ("""CREATE TABLE IF NOT EXISTS vaccine_symptom_data(
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

vaccine_manu_data_create = ("""CREATE TABLE IF NOT EXISTS vaccine_manu_data(
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

article_copy = (f"""copy staging_covid_article_data from {ARTICLE_DATA}
                          credentials 'aws_iam_role={IAM_ROLE}'
                          DELIMITER ','
                          CSV HEADER""")

vac_tweet_copy = (f"""copy staging_covid_vaccine_tweets from {VAC_TWEETS}
                          credentials 'aws_iam_role={IAM_ROLE}'
                          DELIMITER ','
                          CSV HEADER""")

covid_tweet_copy = (f"""copy staging_covid_tweets from {COVID_TWEETS}
                          credentials 'aws_iam_role={IAM_ROLE}'
                          DELIMITER ','
                          CSV HEADER""")


vaccine_data_copy = (f"""copy vaccine_data from {VAC_RESPONSE}
                          credentials 'aws_iam_role={IAM_ROLE}'
                          DELIMITER ','
                          CSV HEADER""")


vaccine_manu_copy = (f"""copy vaccine_manu_data from {VAC_RESPONSE}
                          credentials 'aws_iam_role={VAC_TYPE}'
                          DELIMITER ','
                          CSV HEADER""")


vaccine_symptom_copy = (f"""copy vaccine_symptom_data from {VAC_SYMPTOMS}
                          credentials 'aws_iam_role={IAM_ROLE}'
                          DELIMITER ','
                          CSV HEADER""")

# POPULATE FINAL TABLES

covid_tweet_insert = ("""INSERT INTO covid_tweets(user_name, user_location, date, text)
                            SELECT user_name, user_location, date, text
                            FROM staging_covid_vaccine_tweets
""")

covid_vac_tweet_insert = ("""INSERT INTO covid_vaccine_tweets(user_name, user_location, date, text)
                            SELECT user_name, user_location, date, text
                            FROM staging_covid_vaccine_tweets
""")

article_insert = ("""INSERT INTO users(cord_uid, title, abstract, publish_time, authors)
                        SELECT cord_uid, title, abstract, publish_time, authors
                        FROM staging_covid_article_data
""")

# QUERY LISTS

drop_table_queries = [staging_covid_tweets_drop, covid_tweets_drop, staging_covid_vaccine_tweets_drop, covid_vaccine_tweets_drop,
               staging_covid_article_data_drop, covid_article_data_drop, vaccine_data_drop, vaccine_response_data_drop, vaccine_symptom_data_drop]
create_table_queries = [staging_covid_article_data_create, staging_covid_vaccine_tweets_create, staging_covid_tweets_create, covid_vaccine_tweets_create,
               covid_tweets_create, covid_article_data_create, vaccine_data_create, vaccine_symptom_data_create, vaccine_manu_data_create]
copy_table_queries = [article_copy, vac_tweet_copy, vaccine_data_copy, vaccine_manu_copy, vaccine_symptom_copy]
insert_table_queries = [covid_tweet_insert, covid_vac_tweet_insert, article_insert]
