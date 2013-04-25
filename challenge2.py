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

cs = pyrax.cloudservers

# define image and flavor
flavor_512 = 2
id_of_server = "a997bb89-c33a-4571-81a9-8f676258941a"

print "1"
server = cs.servers.get(id_of_server)
print "2"
new_img = server.create_image("deleteme13")
print "3"
print new_img
print "-Waiting for image creation."
img = pyrax.cloudservers.images.get(new_img)
while img.status != "ACTIVE":
	time.sleep(60)
	img = pyrax.cloudservers.images.get(new_img)
	print "...still waiting"

print "-Image created."


# create server based on new image
newserver = cs.servers.create("challenge2_server", new_img, flavor_512)

# server info print out
print "Admin password:", newserver.adminPass
while not (newserver.networks):
	newserver = cs.servers.get(server.id)
print "Networks:", newserver.networks
