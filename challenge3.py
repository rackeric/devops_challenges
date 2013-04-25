#!/usr/bin/python
#
# · Challenge 3: Write a script that accepts a directory as an argument as well as a container name. The script should upload the contents of the specified directory to the container (or create it if it doesn't exist). The script should handle errors appropriately. (Check for invalid paths, etc.) Worth 2 Points
#
import pyrax
import os
import time

# auth
cred = os.path.join(os.path.expanduser('~'), ".rackspace_cloud_credentials")
pyrax.set_credential_file(cred)

# create objects
cnw = pyrax.cloud_networks
cs  = pyrax.cloudservers
cbs = pyrax.cloud_blockstorage
clb = pyrax.cloud_loadbalancers
dns = pyrax.cloud_dns

ubu_image = "5cebb13a-f783-4f8c-8058-c4182c724ccd"
flavor_512 = 2
