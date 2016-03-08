from django.test import TestCase

# Create your tests here.t
temp = "+1347s5838019"
try:
    float(str(temp.split("+")[1]))
    print "valid"
except ValueError:
    print "Invalid"
