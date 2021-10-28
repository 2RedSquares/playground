# Databricks notebook source
import configparser
import json
from pyspark.sql.functions import get_json_object, json_tuple

# COMMAND ----------

# DBTITLE 1,Read job state
config = configparser.ConfigParser()
config.read('/tmp/config.ini')
database_name = config['DEFAULT']['database_name']
congress_json = config['CONGRESS_MEMBERS']['congress_file']

# COMMAND ----------

with open(congress_json, "r") as f:
  data = json.load(f)

congress = json.loads(data)
congress_array = congress.get("results")[0].get("members")

f = open("/tmp/temp.json", "w")
f.write(json.dumps(congress_array))
f.close()




# COMMAND ----------

# MAGIC %sh
# MAGIC 
# MAGIC less "/tmp/temp.json"

# COMMAND ----------

df = spark.read.json("file:///tmp/temp.json")
df.createOrReplaceTempView("congress")
display(df)

# COMMAND ----------

spark.sql("CREATE OR REPLACE TABLE {}.congress USING DELTA AS SELECT * FROM congress".format(database_name))