import json
from pprint import pprint
import sqlite3


data_list = []
with  open('patient_data.json') as data_file:
    data_list = json.load(data_file)



conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())
for enterie in data_list:
    print enterie
    # cursor.execute("INSERT INTO HealthNet_patien VALUES()")
