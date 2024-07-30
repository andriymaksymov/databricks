# Databricks notebook source
# MAGIC %md
# MAGIC use #secrets/createScope to create a link to keyvault 
# MAGIC

# COMMAND ----------

spark.conf.set("fs.azure.account.key.stdevweatherstream.dfs.core.windows.net", dbutils.secrets.get(scope="kv-dev-weather", key="s-stdevweatherstream-accesskey"))


# COMMAND ----------

dbutils.fs.ls("abfss://landing@stdevweatherstream.dfs.core.windows.net/openweathermap/Maintal")

# COMMAND ----------

df = spark.read.format('json').load("abfss://landing@stdevweatherstream.dfs.core.windows.net/openweathermap/Maintal/")
display(df)

# COMMAND ----------

df.write.format("delta")\
    .option("overwriteSchema", "true")\
    .saveAsTable("weather_log", mode="overwrite", partitionBy=["y","m","d"])


# COMMAND ----------

# MAGIC %sql
# MAGIC select * from weather_log

# COMMAND ----------

# MAGIC %sql
# MAGIC drop table if exists weather;
# MAGIC
# MAGIC create table weather
# MAGIC using json
# MAGIC --partitioned by (year)
# MAGIC location "abfss://landing@stdevweatherstream.dfs.core.windows.net/openweathermap/Maintal/Maintal_010017.json"
# MAGIC comment "external table for Maintal";
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC select 
# MAGIC     name
# MAGIC ,   from_unixtime(dt, 'yyyy-MM-dd HH:mm:ss')    measure_time
# MAGIC ,   to_timestamp(dt)                            measure_dt
# MAGIC ,   main.temp
# MAGIC ,   main.humidity
# MAGIC ,   main.pressure
# MAGIC ,   wind.deg
# MAGIC ,   wind.speed
# MAGIC from weather

# COMMAND ----------

# MAGIC %sql
# MAGIC describe extended weather_log
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
