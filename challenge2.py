#!/usr/bin/python
#
# Challenge 2: Write a script that clones a server
# (takes an image and deploys the image as a new server).
# Worth 2 Point
#
import pyrax
import os
import time

# auth
cred = os.path.join(os.path.expanduser('~'), ".rackspace_cloud_credentials")
pyrax.set_credential_file(cred)

# define image and flavor
flavor_512 = 2
id_of_server = "a997bb89-c33a-4571-81a9-8f676258941a"

cs = pyrax.cloudservers

server = cs.servers.get(id_of_server)
new_img = server.create_image("deleteme2")

print new_img
print "-Waiting for image creation."
time.wait(360)

# create server based on new image
newserver = cs.servers.create("challenge2_server", new_img, flavor_512)

# server info print out
print "Admin password:", server.adminPass
while not (server.networks):
	server = cs.servers.get(server.id)
print "Networks:", server.networks
