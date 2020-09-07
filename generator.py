import random

fp = open("random.txt","a")
l=['0','1']
for i in range(9600):
    fp.write(random.choice(l))
fp.close()