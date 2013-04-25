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
#id_of_server = [img for img in cs.images.list()
#        if "Ubuntu4nova" in img.name][0]


print "1"
server = cs.servers.get(id_of_server)
print "2"
new_img = server.create_image("deleteme7")
print "3"
print new_img
print "-Waiting for image creation."
pyrax.utils.wait_until(new_img,
			att = "status", \
			desired = "available", \
			callback = None, \
			interval = 30, \
			attempts = 25, \
			verbose = True, \
			verbose_atts = None)

# create server based on new image
newserver = cs.servers.create("challenge2_server", new_img, flavor_512)

# server info print out
print "Admin password:", server.adminPass
while not (server.networks):
	server = cs.servers.get(server.id)
print "Networks:", server.networks
