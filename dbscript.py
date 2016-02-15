import json
from pprint import pprint
import sqlite3
with  open('doctor_data.json') as data_file:
    data = json.load(data_file)

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()
for data in cursor.execute('SELECT * from HealthNet_patient'):
    print data
