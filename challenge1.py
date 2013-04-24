#!/usr/bin/python
#
# Challenge 1
#
# Write a script that builds three 512 MB Cloud Servers
# that following a similar naming convention. (ie., web1, web2, web3)
# and returns the IP and login credentials for each server.
# Use any image you want. Worth 1 point
#
import pyrax
import os

cred = os.path.join(os.path.expanduser('~'), ".rackspace_cloud_credentials")
pyrax.set_credential_file(cred)

# create objects
cs  = pyrax.cloudservers

# define image and flavor
ubu_image = "5cebb13a-f783-4f8c-8058-c4182c724ccd"
flavor_512 = 2

# server creation loop
for i in range(1, 4):
	server = cs.servers.create('web' + str(i), ubu_image, flavor_512)
	print "Admin password:", server.adminPass
	while not (server.networks):
		server = cs.servers.get(server.id)
	print "Networks:", server.networks	
