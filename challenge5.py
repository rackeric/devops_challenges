#!/usr/bin/python
#
# Challenge 5
#
# Write a script that creates a Cloud Database instance.
# This instance should contain at least one database,
# and the database should have at least one user that
# can connect to it.
#
# Worth 1 Point
#
import pyrax
import os

cred = os.path.join(os.path.expanduser('~'), ".rackspace_cloud_credentials")
pyrax.set_credential_file(cred)

cdb = pyrax.cloud_databases

inst = cdb.create("deleteME_instance", flavor="512MB Instance", volume=1)
print inst

pyrax.utils.wait_until(inst,
			att = "status", \
			desired = "ACTIVE", \
			callback = None, \
			interval = 30, \
			attempts = 25, \
			verbose = True, \
			verbose_atts = None)

db = inst.create_database("deleteME_db")
print "DB:", db

user = inst.create_user(name="deleteME_user", password="delPASSword123", database_names=[db])
print "User:", user


