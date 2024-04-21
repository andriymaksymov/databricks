# Databricks notebook source
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

token_credential = DefaultAzureCredential()

blob_service_client = BlobServiceClient(
    account_url="https://stdevweatherstream.blob.core.windows.net",
    credential=token_credential
)

print(blob_service_client.primary_endpoint)


# COMMAND ----------

spark.read.format("json").load("dbfs:/FileStore/tables/answers_035158.json")

# COMMAND ----------

spark.conf.set("fs.azure.account.key.stdevweatherstream.blob.core.windows.net",  "==")

# COMMAND ----------

df = spark.read.format("json").load("wasbs://landing@stdevweatherstream.blob.core.windows.net/openweathermap/Maintal/")
display(df)

# COMMAND ----------

# MAGIC %sql
# MAGIC drop table weather;
# MAGIC
# MAGIC create table weather
# MAGIC using json
# MAGIC location "wasbs://landing@stdevweatherstream.blob.core.windows.net/openweathermap/Maintal/Maintal_010017.json"
# MAGIC comment "external table for Maintal";
# MAGIC
# MAGIC select * from weather;

# COMMAND ----------

# MAGIC %sql
# MAGIC describe extended weather
# MAGIC

# COMMAND ----------

# MAGIC %pip install databricks-sql
# MAGIC
# MAGIC from pyspark.sql import SparkSession
# MAGIC
# MAGIC # Read the data into a DataFrame
# MAGIC df = spark.read.format("json").load("wasbs://landing@stdevweatherstream.blob.core.windows.net/openweathermap/Maintal/")
# MAGIC
# MAGIC # Register the DataFrame as a temporary table
# MAGIC df.createOrReplaceTempView("weather_data")
# MAGIC
# MAGIC # Ingest the data into a table
# MAGIC spark.sql("CREATE TABLE weather_table AS SELECT * FROM weather_data")

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC select * from weather
