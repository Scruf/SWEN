import json
import uuid
from pprint import pprint


with  open('doctor.json') as data_file:
    data = json.load(data_file)



patient_user_name=[]
doctor_data=[]
patient_data =[]
doctor_user_name=[]
for name in data:
    patient_user_name.append(name['first_name'][0]+name['last_name'][0])
    patient_data.append(name)


with open('patient.json') as data:
    doctor_data = json.load(data)

for doc in doctor_data:
    doctor_user_name.append(doc['first_name'][0]+doc['last_name'][0])

counter = 0
for patient in patient_user_name:
    if patient in doctor_user_name:
        patient=patient+str(counter)
        counter = counter+1


for user_name,patient in zip(patient_user_name,patient_data):
    with open('patient_data.json','a') as out:

        names ={
            'user_name':user_name,
            'first_name':patient['first_name'],
            'last_name':patient['last_name'],
            'password':str(uuid.uuid1()).split("-")[0],
            'user_id':str(uuid.uuid1()),
            'username':user_name,
        }
        json.dump(names,out,indent=2)

for user_name,doctor in zip(doctor_user_name,doctor_data):
    with open ('doctor_data.json','a') as out:
        name={
            'user_name':user_name,
            'first_name':doctor['first_name'],
            'last_name':doctor['last_name'],
            'password':str(uuid.uuid1()).split("-")[0],
            'user_id':str(uuid.uuid1()),
            'username':user_name,
        }
        json.dump(name,out,indent=2)
# with open('patient.json','a') as out:
#     for patien in pa
#
# print patient_user_name
