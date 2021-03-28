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