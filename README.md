# COVID Data Review Pipeline

## Purpose
We work at a (fake) department at the CDC.  We've been tasked with understanding what topics are trending with respect to coronavirus in general as well as specifically vaccines.

Specifically there is a concern about if the messaging isn't right on the vaccine - and too much focus is on the adverse reactions, we may not be able to reach herd immunity.

As part of the department, we are looking to ensure that we are monitoring the topics, to help influence messaging and decision making related to the COVID programs here.

We have additional Data Scientists within our department, that have asked for some auxillary data to these tasks to be stored in our database.

## Goal
The goal of the project is to generate a dashboard, that allows our department head to easily review what the topics being discussed over time are.  

There is a desire to do a combination of ML + DL to extract value from the data.

## Repo Files:

### ML Models:
This directory is dedicated to utilizing GPT 2 for generating abstracts for articles from summaries.  A much better approach for this dataset, would be some kind of text retrieval.

GPT is fun though.

## Images:
An image showing the suggested component flow, for how the data lands in RedShift and is processed.  As well as the Data Model, for how we will store it in Redshift.

## Data Investigation:
A file dedicated to the discovery and investigation of our core datasets.

## Pipeline for Processing:
Founder under spark ETL.  After initially exploring the useage of RedShift, it seemed that spark would work better for storing our data due to the nature of the data being primarily text.  Redshift could still be a good choice for a numeric data set in the same domain in the future.


## Thought Process:
We wanted to make our analytic users have easy and fast access to the data, such that they could generate results that would best inform our leadership.  This meant pulling data from a variety of sources, primarily text, and performing their own data transformations on it.  We went with the usage of spark, due to the next of the data being highly text.  Redshift appeared to have character limits and seemed to be a suboptimal choice due to that.  Airflow would be a good choice to implement into our pipeline in the next sprint, for both the case of data collection and data processing, we could run our spark job on a scheduled basis.  Additionally we could tie in our analytics jobs to our DAG tool, ensuring that our leadership is always seeing the most up to date results for their decision making.  The tools we ended up using were relatively basic - S3 for storage pre/post spark, that would be collected from a variety of APIs/endpoints.  The best case would be for the data to be updated on a daily basis, ensuring that our analytics user are able to find the trends as quickly as they appear.  If we fell under the case of the data being increased by 100x - we would likely be able to just scale up the number of nodes and size of our EMR cluster, and be able to handle the additional required processing.  If our pipelines needed to be run at 7am daily, using airflow or another DAG tool, would be a great choice having confidence in a nice UI to view both the runs, and schedule them.  If our data needed access by more than 100 people, we could likely stick with spark, but we may want to look into other distributed databases, such as presto or athena.