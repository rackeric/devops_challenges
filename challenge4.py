#!/usr/bin/python
#
# Challenge 4
#
# Write a script that uses Cloud DNS to create a new A record
# when passed a FQDN and IP address as arguments.
#
import pyrax
import os
import sys

domain_name = str(sys.argv[1])
ip = str(sys.argv[2])

cred = os.path.join(os.path.expanduser('~'), ".rackspace_cloud_credentials")
pyrax.set_credential_file(cred)

dns = pyrax.cloud_dns

try:
    dom = dns.find(name=domain_name)
except exc.NotFound:
    answer = raw_input("The domain '%s' was not found. Do you want to create "
            "it? [y/n]" % domain_name)
    if not answer.lower().startswith("y"):
        sys.exit()
    try:
        dom = dns.create(name=domain_name, emailAddress="sample@example.edu",
                ttl=900, comment="sample domain")
    except exc.DomainCreationFailed as e:
        print "Domain creation failed:", e
    print "Domain created:", dom
    print


rec = {
        "type": "A",
        "name": domain_name,
        "data": ip,
        }

new_rec = dom.add_records(rec)
print new_rec
print
print "-DNS record added."

