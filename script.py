import json
import uuid
from pprint import pprint
import random

with  open('doctor.json') as data_file:
    data = json.load(data_file)

def cell_phone():
    number = "+"
    while len(number) < 12:
        rand_int = random.randint(0,9)
        number =  number + str(rand_int)
    return number

def email(un):
    return un+"@gmail.com"

patient_user_name=[]
doctor_data=[]
patient_data =[]
doctor_user_name=[]
diases_data = []
hospital_names = []
for name in data:
    patient_user_name.append(name['first_name'][0]+name['last_name'][0])
    patient_data.append(name)

with open ('log.json') as data:
    diases_data = json.load(data)
with open('patient.json') as data:
    doctor_data = json.load(data)
with open('hospitals.json') as data:
    hospital_names=json.load(data)
for doc in doctor_data:
    doctor_user_name.append(doc['first_name'][0]+doc['last_name'][0])

counter = 0
for patient in patient_user_name:
    if patient in doctor_user_name:
        patient=patient+str(counter)
        counter = counter+1


for user_name,patient in zip(patient_user_name,patient_data):
    random_int = random.randint(0,len(diases_data)-1)
    random_hospital = random.randint(0,len(hospital_names))
    with open('patient_data.json','a') as out:

        names ={
            'user_name':user_name,
            'first_name':patient['first_name'],
            'last_name':patient['last_name'],
            'password':str(uuid.uuid1()).split("-")[0],
            'email':email(user_name),
            'username':user_name,
            'cell_phone':cell_phone(),
            'diases':diases_data[random_int]['disease_name'],
            'symptoms':diases_data[random_int]['symptoms'],
            'hospital_name':''.join(hospital_names[random_hospital]),
        }
        json.dump(names,out,indent=2)

for user_name,doctor in zip(doctor_user_name,doctor_data):
    random_hospital = random.randint(0,len(hospital_names)-1)
    with open ('doctor_data.json','a') as out:
        name={
            'user_name':user_name,
            'first_name':doctor['first_name'],
            'last_name':doctor['last_name'],
            'email':email(user_name),
            'password':str(uuid.uuid1()).split("-")[0],
            'username':user_name,
            'cell_phone':cell_phone(),
            'hospital_name':''.join(hospital_names[random_int]),
        }
        json.dump(name,out,indent=2)
