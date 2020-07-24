import os
import os.path
from os import path



user_root = "user/"
input = "kane1234"

def user_dir(input):

    print("Full Path: "+user_path)
    if path.isdir(user_root):
        print("Yay! The root path exists")
        if path.isdir(user_path):
            print("OK! The full path exists. Nothing to do.")
        else:
            print("NO! The full path DOES NOT exist yet. Attempting to fix now.")
            try:
                os.mkdir(user_path)
            except OSError:
                    print ("Creation of the directory %s failed" % path)
            else:
                    print ("Successfully created the directory %s " % path)
                    
    else:
        print("UH OH! The User_Root path does not exists")
