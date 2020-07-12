import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


from cryptography.fernet import Fernet
from flask_bcrypt import Bcrypt


# ENCRYPTION METHODS - Fernet / small amounts of infomation
def fkey(input):  # creates keys for users


    salt = os.urandom(6)
    key = input.encode()
    kdf = PBKDF2HMAC(  # settings for key to be made with
        algorithm=hashes.SHA256(),  # hash set to use
        length=12,
        salt=salt,
        iterations=999999,  # more the merrier
        backend=default_backend()  # the backend for this all to put together with
    )

    key = base64.urlsafe_b64encode(kdf.derive(key))  # building it
    return key
def encrypt(input, client_key, server_key):

    if not isinstance(input, bytes):
        input = input.encode()

    key = b"".join([client_key,server_key])
    key = base64.urlsafe_b64encode(key)# building it

    f = Fernet(key)

    encrypted = f.encrypt(input)
    return encrypted
def decrypt(input, client_key, server_key):

    if not isinstance(input, bytes):
        input = input.encode()
            
    key = b"".join([client_key,server_key])
    key = base64.urlsafe_b64encode(key)# building it

    f = Fernet(key)

    decrypted = f.decrypt(input)
    return decrypted




import ipapi
import socket
import json

ip = socket.gethostbyname(socket.gethostname())

geolocate = ipapi.location(ip)
geolocate_str = json.dumps(geolocate).strip('{}').replace('"', '') + ","

if "reserved: true" in geolocate_str:
    print("local ip detected")
print(geolocate_str)



#{% for post in post %}
#  {% if post.private == true and post.user_id == current_user.user_id%}
#    {% set title = ip_list(fdecrypt(post.title, current_user.priv_key))  %}
#    {% set content = ip_list(fdecrypt(post.content, current_user.priv_key))  %}
#    <div class="post_home">
#      <div style="color: white;">
#        <a href="/post/{{post.post_id}}"><h1>{{title}} <span style="font-size:large;"> posted by {{post.author.username}}</span></h1></a>
#        <p>{{content}}</p>
#        {% if post.images %}
#          {% set images = ip_list(fdecrypt(post.images, current_user.priv_key))  %}
#          {{ filext(images) | safe }}
#        {% endif %}
#        <p style="text-align: right;">{{post.posted_date.strftime('%H:%M, %d-%m-%Y')}}</p>
#      </div>
#      <br>
#      {% elif post.private != true %}
#      <div style="color: white;">
#        <a href="/post/{{post.post_id}}"><h1>{{post.title}} <span style="font-size:large;"> posted by {{post.author.username}}</span></h1></a>
#        <p>{{post.content}}</p>
#        {% if post.images %}
#         {{ filext(post.images) | safe }}
#        {% endif %}
#        <p style="text-align: right;">{{ post.posted_date.strftime('%H:%M, %d-%m-%Y') }}</p>
#      </div>
#    </div>
#    <br>
#    {% endif %}
#{% endfor %}