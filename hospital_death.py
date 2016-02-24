hospital_list = []
for h in Hospital.objects.all():
    hospital_list.append(h.id)

while Hospital.objects.count > 5:
    random_hospital = random.randint(1,len(hospital_list)-1)
    Hospital.objects.get(pk=hospital_list[random_hospital]).delete()
    del hospital_list[random_hospital]
