# Databricks notebook source
dbutils.widgets.text(
  name='api_key',
  defaultValue='',
  label='ProPublica API Key'
)

dbutils.widgets.text(
  name='domain_name',
  defaultValue='api.propublica.org',
  label="ProPublica API Domain"
)

dbutils.widgets.text(
  name='congress_number',
  defaultValue='117',
  label="Congress Number"
)

# COMMAND ----------

import requests
import json
import configparser

# COMMAND ----------

api_key = dbutils.widgets.get('api_key')
domain_name = dbutils.widgets.get('domain_name')
congress_number = dbutils.widgets.get('congress_number')

# COMMAND ----------

conn_str = "https://" + domain_name + "/congress/v1/" + congress_number + "/house/members.json"
headers = {'X-API-Key': api_key}
r = requests.get(conn_str, headers=headers)
congress_json = r.text
print(congress_json)

# COMMAND ----------

congress_json = '/tmp/congress_{}.json'.format(congress_number)

with open(congress_json, 'w') as outfile:
    json.dump(r.text, outfile)

# COMMAND ----------

config = configparser.ConfigParser()
config.read('/tmp/config.ini')
config['CONGRESS_MEMBERS'] = {'congress_file': congress_json}

with open('/tmp/config.ini', 'w') as configfile:
    config.write(configfile)

# COMMAND ----------

# MAGIC %sh
# MAGIC 
# MAGIC less /tmp/config.ini