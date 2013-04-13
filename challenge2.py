#!/usr/bin/python
#
# Challenge 2: Write a script that clones a server
# (takes an image and deploys the image as a new server).
# Worth 2 Point
#
import pyrax
import time

username = "utcodemonkey"
API_key = "25136ca5cbe07aa925da1ee2f232aa5a"

pyrax.set_credentials(username, API_key)

flavor_512 = 2
id_of_server = "9d4b35ac-d91d-48da-8c32-1d8c6744fa7b"

cs = pyrax.cloudservers

server = cs.servers.get(id_of_server)
new_img = server.create_image("challenge2")
newserver = cs.servers.create("challenge2", new_img, flavor_512)
