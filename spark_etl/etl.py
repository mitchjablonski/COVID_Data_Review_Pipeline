import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col, monotonically_increasing_id
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format, dayofweek
from pyspark.sql.types import TimestampType
import posixpath


config = configparser.ConfigParser()
config.read('covid_pipeline.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config['AWS']['KEY']
os.environ['AWS_SECRET_ACCESS_KEY']=config['AWS']['SECRET']


def create_spark_session():
    '''
    Create a spark session if none exists, or grab the existing session
    '''
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark


def process_tweet_data(spark, input_data, output_data):
    '''
    Takes in our spark instance, and an input and output data path.
    
    We'll take the columns of interest from both file and write these to our desired tables.
    '''
    # get filepath to covid tweet data file
    covid_data = posixpath.join(input_data, 'covid_twitter/2021-03-24_clean-dataset_short.json')
    # read covid tweet data file
    df = spark.read.json(covid_data)
    
    # extract columns to create covid tweet table
    tweet_table = df.select('user_name', 'user_location', 'date', 'text').filter(col('text').isNotNull()).drop_duplicates()
    tweet_table = tweet_table.withColumn('tweet_id', monotonically_increasing_id())
    
    # write songs table to parquet files partitioned by year and artist
    tweet_table.write.parquet(posixpath.join(output_data, "covid_tweets/"), mode="overwrite", partitionBy=["date"])


    # get filepath to covid vaccine tweet data file
    vac_data = posixpath.join(input_data, 'vaccine_tweets/covidvaccine_tweets.csv')
    df = spark.read.csv(vac_data)
    
    # extract columns to create covid vaccome tweet table
    tweet_table = df.select('user_name', 'user_location', 'date', 'text').filter(col('text').isNotNull()).drop_duplicates()
    tweet_table = tweet_table.withColumn('tweet_id', monotonically_increasing_id())
    
    # write songs table to parquet files partitioned by year and artist
    tweet_table.write.parquet(posixpath.join(output_data, "covid_vac_tweets/"), mode="overwrite", partitionBy=["date"])


def process_vaccine_response_data(spark, input_data, output_data):
    '''
    Takes in our spark instance, and an input and output data path.
    
    We'll take the columns of interest from both file and write these to our desired tables.
    '''

    # get filepath to log data file
    vaers_response =posixpath.join(input_data, 'vaccine_response_data/2021VAERSDATA.csv')

    # read log data file
    df = spark.read.csv(vaers_response)
    
    # extract columns for users table    
    vares_response_table = df.select(col("VAERS_ID"), col("STATE"), 
                            col("AGE_YRS"),col("RPT_DATE"),col("SYMPTOM_TEXT"),
                            col("VAX_DATE")).filter(col('userId').isNotNull()).drop_duplicates()
    
    # write users table to parquet files
    vares_response_table.write.parquet(posixpath.join(output_data, "vaers_response/"), mode="overwrite")

    # get filepath to log data file
    vaers_symptoms =posixpath.join(input_data, 'vaccine_response_data/2021VAERSSYMPTOMS.csv')

    # read log data file
    df = spark.read.csv(vaers_symptoms)
    
    # extract columns for users table    
    vaers_symptoms_table = df.select(col("VAERS_ID"), col("SYMPTOM1"), 
                            col("SYMPTOMVERSION1"),col("SYMPTOM2"),col("SYMPTOMVERSION2"),
                            col("SYMPTOM3"), col('SYMPTOMVERSION3'),
                            col("SYMPTOM4"), col('SYMPTOMVERSION4'),
                            col("SYMPTOM5"), col('SYMPTOMVERSION5')).drop_duplicates()
    
    # write users table to parquet files
    vaers_symptoms_table.write.parquet(posixpath.join(output_data, "vaers_symptoms/"), mode="overwrite")

    vaers_vax =posixpath.join(input_data, 'vaccine_response_data/2021VAERSVAX.csv')
    # read log data file
    df = spark.read.csv(vaers_vax)
    
    # extract columns for users table    
    vaers_vax_table = df.select(col("VAERS_ID"), col("VAX_TYPE"), 
                            col("VAX_MANU"),col("VAX_LOT"),col("VAX_DOSE_SERIES"),
                            col("VAX_ROUTE"), col('VAX_SITE'),
                            col("VAX_NAME")).drop_duplicates()
    
    # write users table to parquet files
    vaers_vax_table.write.parquet(posixpath.join(output_data, "vaers_vax/"), mode="overwrite")

def process_article_data(spark, input_data, output_data):
    # get filepath to log data file
    article_data =posixpath.join(input_data, 'article_metadata/metadata.csv')

    # read log data file
    df = spark.read.csv(article_data)
    # extract columns for users table    
    vaers_symptoms_table = df.select(col("cord_uid"), col("title"), 
                            col("abstract"),col("authors"),col("publish_time"),
                            col("url")).filter(col('title').isNotNull()).filter(col('abstract').isNotNull()).drop_duplicates()
    # write users table to parquet files
    vaers_symptoms_table.write.parquet(posixpath.join(output_data, "article_metadata/"), mode="overwrite")

def main():
    '''
    Our main function for kicking off our processing pipeline.
    '''
    spark = create_spark_session()
    input_data = "s3a://udacity-capstone-data"
    output_data = "s3a://udacity-capstone-data-processed"
    
    process_tweet_data(spark, input_data, output_data)    
    process_vaccine_response_data(spark, input_data, output_data)
    process_article_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()