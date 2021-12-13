import pandas as pd
import numpy as np
import datetime as dt
import json
import sqlite3
from sqlalchemy import create_engine

with open('sample-data.json', mode = 'r', encoding = 'utf-8') as file:
    data = json.load(file)

#načtení dat
vstup = pd.DataFrame(data)

#tvorba prázdného dataframu
vystup = pd.DataFrame(columns = ['name', 'cpu_use', 'memory_use', 'created_at', 'status', 'IP'])

#zápis dat do df
vystup.name = vstup.name

for i,e in enumerate(vstup.state):
    try:
        vystup.memory_use[i] = vstup.state[i]['memory']['usage']
    except:
        pass

for i, e in enumerate(vstup.created_at):
    vystup.created_at[i] = pd.to_datetime(vstup.created_at[i]).tz_convert('UTC')

vystup.status = vstup.status

for i,e in enumerate(vstup.state):
    try:
        network = pd.DataFrame.from_dict(vstup.state[i]['network'])
    except:
        pass
    ips = []
    for j in network.loc['addresses']:
        for k in j:
            ips.append(k['address'])
    vystup.IP[i] = ips

#převedu IP a datum na string
vystup.IP = vystup.IP.apply(str)
vystup.created_at = vystup.created_at.apply(str)

#zapíšu do databáze
connection = sqlite3.connect("Teska.db")
engine = create_engine('sqlite://', echo=False)
vystup.to_sql('vystup', con=connection, index = False)



