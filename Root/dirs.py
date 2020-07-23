import os
import os.path
from os import path

usr = "usr/"
user_id = "117"

user_path = usr+user_id

print(user_path)
if path.isdir("usr/"):
    if path.isdir(user_path):
        print(user_path+" does exist")

    else:

        try:
            os.mkdir(user_path)

        except OSError:
            print ("Creation of the directory %s failed" % path)
        else:
            print ("Successfully created the directory %s " % path)
else:
    print("does not exists")


"""  
try:
    os.mkdir(path)

except OSError:
        print ("Creation of the directory %s failed" % path)
else:
    print ("Successfully created the directory %s " % path)
"""