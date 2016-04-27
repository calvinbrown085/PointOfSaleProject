import os
from random import randint

def generateKey():
    try:
        return os.environ["Key"]
    except:
        return generatRandomString(20)

def generatRandomString(length):
    string = ""
    for i in range(0,length):
        x = randint(0,1)
        if (x == 0):
            string += chr(randint(97,122))
        elif (x == 1):
            string += chr(randint(97,122)).upper()
    return string
