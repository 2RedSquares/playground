# Databricks notebook source
# DBTITLE 1,Define input parameters
dbutils.widgets.text(
  name='database_name',
  defaultValue='us_congress',
  label='Database Name'
)

dbutils.widgets.text(
  name='project_home',
  defaultValue='/home/scott.stafford@databricks.com/us_congress',
  label="Project Home"
)

# COMMAND ----------

import configparser
import os

# COMMAND ----------

# DBTITLE 1,Get Input Parameters
database_name = dbutils.widgets.get('database_name')
project_home = dbutils.widgets.get('project_home')

# COMMAND ----------

# MAGIC %sh
# MAGIC 
# MAGIC ls /dbfs/home/scott.stafford@databricks.com/us_congress/

# COMMAND ----------

config = configparser.ConfigParser()
config['DEFAULT'] = {
  'database_name': database_name,
  'project_home': project_home
}

with open('/tmp/config.ini', 'w') as configfile:
    config.write(configfile)

# COMMAND ----------

spark.sql("SET database_name={}".format(database_name))
spark.sql("SET project_home={}".format(project_home))

# COMMAND ----------

# MAGIC %sql 
# MAGIC CREATE DATABASE IF NOT EXISTS ${database_name} LOCATION "${project_home}/db";

# COMMAND ----------

# MAGIC %sh
# MAGIC 
# MAGIC 
# MAGIC less /tmp/config.ini