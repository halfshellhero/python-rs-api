#!/usr/bin/env python

import os, sys, time
import argparse
import pyrax

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('instancename')
    parser.add_argument('databasename')
    parser.add_argument('username')
    parser.add_argument('--flavor', type=int, default=1)
    parser.add_argument('--volumesize', default=1)
    parser.add_argument('--password')
    args = parser.parse_args()
    
    if args.password is None:
	args.password = pyrax.utils.random_name(length=10, ascii_only=True)




    creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
    pyrax.set_credential_file(creds_file)
    cdb = pyrax.cloud_databases

    db_dicts = [{"name": args.databasename}]
    body = [
                    {"name": args.username,
                    "password": args.password,
                    "databases": db_dicts,
                    }]

    instance = cdb.create(args.instancename, flavor=args.flavor, volume=args.volumesize, users=body, databases=db_dicts)

    print "Name:", instance.name
    print "ID:", instance.id
    print "Username:", args.username
    print "Password:", args.password
    print "Status:", instance.status
    print "Flavor:", instance.flavor.name

if __name__ == "__main__":
    main()
