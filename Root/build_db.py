from Blog import db
from Blog.model import User,Post

import os
if os.path.exists("Blog/blog.db"):
  os.remove("Blog/blog.db")
else:
  print("The file does not exist") 
  db.create_all()


exit()

