#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2012 Rackspace

# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os
import pyrax
import time

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
cs = pyrax.cloudservers
name = str(raw_input ("Please enter server naming scheme: "))

ubu_image = [img for img in cs.images.list()
        if "12.04" in img.name][0]
flavor_512 = [flavor for flavor in cs.flavors.list()
        if flavor.ram == 512][0]

servers = {}

i = 1

while (i <= 3):
	server_name = name + str(i)
	servers[server_name] = cs.servers.create(server_name, ubu_image.id, flavor_512.id)
	i = i + 1

for x,y in servers.items():
	print "Name:", servers[x].name
	print "Admin Password:", servers[x].adminPass
	print "Waiting for networking..."
	
	isnetworking = servers[x].networks
	while not 'public' in isnetworking:
		time.sleep(10)
		servers[x].get()
		isnetworking = servers[x].networks

	print "Networks:", servers[x].networks

	print ""
