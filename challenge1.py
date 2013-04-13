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
import time

username = ""
API_key = ""

pyrax.set_credentials(username, API_key)

# create objects
cs  = pyrax.cloudservers

# define image and flavor
ubu_image = "5cebb13a-f783-4f8c-8058-c4182c724ccd"
flavor_512 = 2

# server creation loop
for i in range(1, 4):
	#name = 'web' + str(i)
	#print name
	server = cs.servers.create('web' + str(i), ubu_image, flavor_512)
	while not (server.networks):
		server = cs.servers.get(server.id)
	print "Admin password:", server.adminPass
	print "Networks:", server.networks	
