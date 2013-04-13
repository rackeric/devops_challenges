#!/usr/bin/python
#
# Challenge 11
#
# Challenge 11: Write an application that will:
# Create an SSL terminated load balancer (Create self-signed certificate.)
# Create a DNS record that should be pointed to the load balancer.
# Create Three servers as nodes behind the LB.
#     Each server should have a CBS volume attached to it. (Size and type are irrelevant.)
#     All three servers should have a private Cloud Network shared between them.
#     Login information to all three servers returned in a readable format as the result of the script, including connection information.
# Worth 6 points
#
import pyrax
import time

username = "utcodemonkey"
API_key = "25136ca5cbe07aa925da1ee2f232aa5a"

pyrax.set_credentials(username, API_key)

# create objects
cnw = pyrax.cloud_networks
cs  = pyrax.cloudservers
cbs = pyrax.cloud_blockstorage
clb = pyrax.cloud_loadbalancers
dns = pyrax.cloud_dns

ubu_image = "5cebb13a-f783-4f8c-8058-c4182c724ccd"
flavor_512 = 2

print "\n"
print "-Creating CS server and CNW network.\n"
# create isolated network
my_network = cnw.create("challenge11_net", cidr="192.168.200.0/24")
# get listing of networks for server creation
networks_list = my_network.get_server_networks(public=True, private=True)

# create 3 servers, no loop
server1 = cs.servers.create("server1", ubu_image, flavor_512, networks=networks_list)
server2 = cs.servers.create("server2", ubu_image, flavor_512, networks=networks_list)
server3 = cs.servers.create("server3", ubu_image, flavor_512, networks=networks_list)
print "-Cloud Servers and isolated Cloud Network created. 192.168.200.0/24\n"
# print server info
print "Server uuid: ", server1.id
print "Admin password: ", server1.adminPass
print "Server uuid: ", server2.id
print "Admin password: ", server2.adminPass
print "Server uuid: ", server3.id
print "Admin password: ", server3.adminPass

# wait for networks to be assigned
while not (server1.networks and server2.networks and server3.networks):
	time.sleep(1)
	server1 = cs.servers.get(server1.id)
	server2 = cs.servers.get(server2.id)
	server3 = cs.servers.get(server3.id)

# get server private IPs
server1_ip = server1.networks["private"][0]
server2_ip = server2.networks["private"][0]
server3_ip = server3.networks["private"][0]

# use IPs to create nodes for CLB
node1 = clb.Node(address=server1_ip, port=80, condition="ENABLED")
node2 = clb.Node(address=server2_ip, port=80, condition="ENABLED")
node3 = clb.Node(address=server3_ip, port=80, condition="ENABLED")

# create VIP for CLB
vip = clb.VirtualIP(type="PUBLIC")

# create the CLB
lb = clb.create("challenge11_LB", port=80, protocol="HTTP", nodes=[node1,node2,node3], virtual_ips=[vip])

cert = "-----BEGIN CERTIFICATE-----\nMIIDEzCCAfugAwIBAgIJANP7xqPWRkJfMA0GCSqGSIb3DQEBBQUAMCAxHjAcBgNV\nBAMMFW5vdmEuZW1wdWxzZWdyb3VwLmNvbTAeFw0xMzA0MTExNTQ0NTJaFw0yMzA0\nMDkxNTQ0NTJaMCAxHjAcBgNVBAMMFW5vdmEuZW1wdWxzZWdyb3VwLmNvbTCCASIw\nDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBANwgRXqbZk/c3d9fclejgkZvrqpp\nOCvB7IuTlmnOylJg5oxBVGNA5/AQXumTudfix08vg6PojHf1LRiZIDn1vSPmgtIO\nbxhaLddya7VzprPYjor+IpKlubTNzHNRubR+Dgndo7F+CBQqbi1IPDtEbNXsdZ8q\nkX8e1HsJvfClCJVuBNruE33JMdJ4BSIvalQCARbPZGsne1X3BH8XPzTDKEolm3Uw\nYlG4YvW6/j9mgf58bbkNs45VELa2Z6Z/J8SxGN8tTf86jc1hMsVWR2Oubh7IJOC2\nP5HU+ljG7Sneqg0i6QisYrmqkfH5sJdiB26f/QPg1CxZrNDZoJYFqyvsr1UCAwEA\nAaNQME4wHQYDVR0OBBYEFIu/FtlKzicwkskNJgV5nWSo/1azMB8GA1UdIwQYMBaA\nFIu/FtlKzicwkskNJgV5nWSo/1azMAwGA1UdEwQFMAMBAf8wDQYJKoZIhvcNAQEF\nBQADggEBANBttJkQZ+pDJyqnDmq4gHpBUOR4phfCUN624hXSLi0F8i6M5+UwjRGS\nk4MRgXZti/jTDqVa0G7RkFvJ4A/NXJMltzqbeTqulz+uXhTtNtCO3A4iBBtuzlJt\nVdIcbC+89WxOXLICJbNnYjdsvBLb/75JKDCBc5igNYO4EyJgEMF7VnC1uYzr3kUA\nhKGfhDZ08lYCeNNifFM/vRdm/3Y01sGMiF8GwvGMO6+gfmsKEz0gan/yHiGVpgxZ\novOpCwevjwtWqJfyQ70zE/QZUc+onIyl5SV4VjmclyIHlYu4gfg2UqT+Zv123qOd\nMtYSbTBtOXrtuBHEDRQ0W3dmJrOEUkY=\n-----END CERTIFICATE-----"

pk = "-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEA3CBFeptmT9zd319yV6OCRm+uqmk4K8Hsi5OWac7KUmDmjEFU\nY0Dn8BBe6ZO51+LHTy+Do+iMd/UtGJkgOfW9I+aC0g5vGFot13JrtXOms9iOiv4i\nkqW5tM3Mc1G5tH4OCd2jsX4IFCpuLUg8O0Rs1ex1nyqRfx7Uewm98KUIlW4E2u4T\nfckx0ngFIi9qVAIBFs9kayd7VfcEfxc/NMMoSiWbdTBiUbhi9br+P2aB/nxtuQ2z\njlUQtrZnpn8nxLEY3y1N/zqNzWEyxVZHY65uHsgk4LY/kdT6WMbtKd6qDSLpCKxi\nuaqR8fmwl2IHbp/9A+DULFms0NmglgWrK+yvVQIDAQABAoIBADHN62puNpvjMSAV\nDF3f1N3y7uYHoHnmCosZ/XI7I3O4EPGy5lD+onuieJcIoYfC+61i5rnzJ7UMeAOU\nwcHbY8v3n6m/MkukO7L/ZHdNj24plTbFgTUE4huSZKvC1e2Mh8ibqSnDhjhp0TvV\nmCsgtC9CrOoyS3EjnJeqAJut+18zdeGlcvV8VXzz9jRXXC8ytBaZpZcnTw+uKhfO\nWxEEv6OcKGVTE6zZaE6WmmMr0DJAO9VOQE84KilKBcmj90s7ZNi7qYMQrFDJ5t4s\nA0S4HVh44GcTrZvTREtfFWXoQjiRwPrw3ZPIWpbGpmXRXNz7+oh28Pj3gL3aZkl1\n6anLXgECgYEA7qhRiIGtuFRkyNmcXwCBT09pzwhpKuALk6CRvRhnfHx4Pax92myx\nSD5oiTzwRW+u0jsY44aKO/1N96izJZAlH63ebIM7vZLtH+vdYYUxMIzfDEEuOehl\n/O0H3VOclf62ldTT+za3fX+61l8FeDFgirwEzF20nraspZnKXNcpHiECgYEA7B83\ntP2jiaFFHDwvl0OAFdJ8O0AhKvqytpWWhB/QcA/FDaaFw35RqukQJN7/MMhAn3iI\no5m0bqFxBEQRdyKdPJdv2h34DmzCQPq1b/k5vBM4A9Zcx5Y4XNBxxaal702LB4Cb\nR1GtbYv7o2Et5hMJ3YVdfY24tQ/4SUzRzLaaIrUCgYEA0oid1IRBkfixKBYAQjaZ\n3DM8Li1HSVF4JPVjW6Mpt8G9+Pov0/5KrmaPpXGirD6HxGHp5N2NGLquiynBUAPH\nHBkvvB5RFz2D/cL++saazC+ZnJ/rfZ4sSmF3rKHT4uZef/LORjDQ0d9aHT6Z/pvg\nhMK0oOyRJ+oSh8wRnrEYTsECgYAgefK5jCFQLsRIq+aH0ZruZXL820c0mCK4hj6b\nkZyjrSeXRw4i417sOP4ldB55YTGyPWvdxKhShxX6VjpovnQN/248+95AbakSMul9\nqzPLsIEF1hgQw5KhAXKEkvVDwtCaiY/R8WP/Kz/DKvybJoc21r8TI8kB7l5iBpTc\nqUjt+QKBgBIdNl1xqOm9N75Ij/rOu0fCObLeIUuu23aRSGBkYHxZeNd+GM2y5kZk\naWRT3nZ6uUnAy8ITNzxt8L2o5nQVtpUuZrumSjdZaA5mZf+WYYjwCPelLcVoOCEN\nZC0lb7Sq8lt4nJTLcodIW09ldXtalbftnWgzwi68P/ntDdxVj86N\n-----END RSA PRIVATE KEY-----"

# SSL termination for the CLB
#time.sleep(30)
print "-CLB created, waiting for activation.\n"
pyrax.utils.wait_until(lb,
			att = "status", \
			desired = "ACTIVE", \
			callback = None, \
			interval = 15, \
			attempts = 25, \
			verbose = True, \
			verbose_atts = None)
print "-CLB now active.\n"
lb.add_ssl_termination(securePort=443, enabled=True, secureTrafficOnly=False, certificate=cert, privatekey=pk)
print "SSL termination now active.\n"
# print CLB info
print [(lb.name, lb.id) for lb in clb.list()]

print "-Creating CBS volumes.\n"
# create CBS volumes
vol1 = cbs.create(name="vol1", size=100, volume_type="SATA")
vol2 = cbs.create(name="vol2", size=100, volume_type="SATA")
vol3 = cbs.create(name="vol3", size=100, volume_type="SATA")

print "-Waiting for CBS volumes activation.\n"
time.sleep(120)
# attach CBS volumes to servers
mountpoint = "/dev/xvdb"
vol1.attach_to_instance(server1, mountpoint=mountpoint)
vol2.attach_to_instance(server2, mountpoint=mountpoint)
vol3.attach_to_instance(server3, mountpoint=mountpoint)
print "-CBS volumes now attached.\n"

# list networks
for net in cnw.list():
	print net.label, net.cidr, net.id


# DNS
dom = dns.create(name="empnew.com", emailAddress="admin@empnew.com")

recs = [{
        "type": "A",
        "name": "empnew.com",
        "data": lb.virtual_ips[0].address,
        }, {
        "type": "A",
        "name": "www.empnew.com",
        "data": lb.virtual_ips[0].address,
        }]

dom.add_records(recs)
print "-DNS record added."
