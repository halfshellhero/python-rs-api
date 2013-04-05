#!/usr/bin/env python

import argparse, sys, os, time
import pyrax

def main():

	creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
	pyrax.set_credential_file(creds_file)
	cf = pyrax.cloudfiles
	dir_name = ''
	cont_name = ''

	parser = argparse.ArgumentParser()
	parser.add_argument('-d', '--directory', required=True)
	parser.add_argument('-c', '--container', required=True)
	
	args = parser.parse_args()
	cont_name = args.container
	dir_name = args.directory

	print 'Source directory is: ', dir_name
	print 'Destination container is: ', cont_name

	all_containers = cf.list_containers()
	if cont_name not in all_containers:
		print "This container does not exist.  Creating now..."
		cont = cf.create_container(cont_name)

	while os.path.exists(dir_name) == False:
		print "This path/folder does not exist.  Please check your path again."
		dir_name = str(raw_input ("Please enter the directory to be uploaded: "))

	upload_key, total_bytes = cf.upload_folder(dir_name, cont_name)

	print "Total bytes to upload:", total_bytes
	uploaded = 0
	while uploaded < total_bytes:
		uploaded = cf.get_uploaded(upload_key)
		print "Progress: %4.2f%%" % ((uploaded * 100.0) / total_bytes)
		time.sleep(1)

	print "Upload complete!"
if __name__ == "__main__":
	main()
