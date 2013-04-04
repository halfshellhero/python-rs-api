#!/usr/bin/env python

import os
import sys
import pyrax
import time

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
cs = pyrax.cloudservers
servers = cs.servers.list()
srv_dict = {}
print "Select a server from which an image will be created."
for pos, srv in enumerate(servers):
    print "%s: %s" % (pos, srv.name)
    srv_dict[str(pos)] = srv.id
selection = None
while selection not in srv_dict:
    if selection is not None:
        print "   -- Invalid choice"
    selection = raw_input("Enter the number for your choice: ")

server_id = srv_dict[selection]
print
nm = raw_input("Enter a name for the image: ")

img_id = cs.servers.create_image(server_id, nm)

print "Image '%s' is being created. Its ID is: %s" % (nm, img_id)

imagestatus = cs.images.get(img_id)

while imagestatus.status != 'ACTIVE':
	print "Waiting on image to become active..."
	time.sleep(60)
	imagestatus = cs.images.get(img_id)

	# Bomb out if image status goes to ERROR
	if imagestatus.status == 'ERROR':
		print "The imaging process has failed.  Please try again."
		sys.exit()

orig_server_id = cs.servers.get(server_id)

#need to replace the '2' with a variable
flavor = orig_server_id.flavor['id']


print ""
clonename = raw_input("Enter the name for your new server: ")

print "Creating your clone now..."
newserver = cs.servers.create(clonename, img_id, flavor)


print "Name:", newserver.name
print "Admin Password:", newserver.adminPass
print "Waiting for networking..."

isnetworking = newserver.networks

while not 'public' in isnetworking:
	time.sleep(10)
	newserver.get()
	isnetworking = newserver.networks


print "Networks:", newserver.networks
