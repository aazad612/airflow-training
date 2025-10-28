# Airflow Training
Initially created for a Apache Airflow 2.3, in the process of building an Airflow 3.1 training. 

# Folders

## 2.0
Very useful if you are still using the older version, especially the tuning.sh has parameters that need to be changed in GKE or VM based setups. 

## 3.1
All new work would be put in here. 

# Completed work

## 3.1/vm/airflow-install.md

Cloud composer is the managed version of Apcahce Airflow and easiest way to get started. But it is not the ideal solution from a cost perspective, so we will install it on a single VM instance on Google Cloud. 

## IMDB data ingestion pipelines
We will extract the data from IBDB public website everyday, convert the TSV files into parquet and load into BQ using Apache beam using python as well as Java. 

## Terraform Deployment
All working except 
1. bq_ext.tf
2. Issue with authentication on macbook with json key. 

## Daily ingestion dag is working correctly 

## Beam and transformation dags pending. 