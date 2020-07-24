from Blog import db
from Blog.model import User,Post

import os
if os.path.exists("Blog/blog.db"):
  os.remove("Blog/blog.db")
else:
  print("The file does not exist") 
  db.create_all()

from Blog import app

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="5000")


