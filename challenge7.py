#!/usr/bin/env python

import os
import pyrax
import time

def main():

     creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
     pyrax.set_credential_file(creds_file)
     cs = pyrax.cloudservers
     clb = pyrax.cloud_loadbalancers
     lb_name = pyrax.utils.random_name(length=8,ascii_only=True)

     name = str(raw_input ("Please enter server naming scheme for your two servers: "))
     
     ubu_image = [img for img in cs.images.list()
             if "12.04" in img.name][0]
     flavor_512 = [flavor for flavor in cs.flavors.list()
             if flavor.ram == 512][0]
     
     servers = {}
     
     i = 1
     
     while (i <= 2):
     	server_name = name + str(i)
     	servers[server_name] = cs.servers.create(server_name, ubu_image.id, flavor_512.id)
     	i = i + 1
     
     for x,y in servers.items():
     	print "Name:", servers[x].name
     	print "Admin Password:", servers[x].adminPass
     	print "Waiting for networking..."
     	
     	isactive = servers[x].status
     	while not 'ACTIVE' in isactive:
     		time.sleep(10)
     		servers[x].get()
     		isactive = servers[x].status
     
     	print "Networks:", servers[x].networks
     
     	print ""

     nodes = [clb.Node(address=server.networks['private'][0], port=80, condition="ENABLED") for server in servers.values()]
     vip = clb.VirtualIP(type="PUBLIC")
     lb = clb.create(lb_name, port=80, protocol="HTTP", nodes=nodes, virtual_ips=[vip])

     print
     print "Load Balancer:", lb

if __name__ == "__main__":
    main()
