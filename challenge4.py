#!/usr/bin/env python

import os, sys, argparse, time
import pyrax
import pyrax.exceptions as exc


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--fqdn', required=True)
    parser.add_argument('--ip', required=True)

    args = parser.parse_args()
    fqdn = args.fqdn
    ip = args.ip

    print fqdn
    print ip

    creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
    pyrax.set_credential_file(creds_file)
    dns = pyrax.cloud_dns

    try:
        dom = dns.find(name=fqdn)
    except exc.NotFound:
        answer = raw_input("The domain " + fqdn + " was not found.  Do you want to create it? [y/n]")
        if not answer.lower().startswith("y"):
            sys.exit()
        try:
            email = raw_input("Please enter an email address to associate with this domain: ")
            dom = dns.create(name=fqdn, emailAddress=email, ttl=900)
        except exc.DomainCreationFailed as e:
            print "Domain creation failed:", e
        print "Domain created:", dom
        print

    a_rec = {"type": "A",
            "name": fqdn,
            "data": ip,
            "ttl": 300}

    records = dom.add_records([a_rec])
    print records
    print


if __name__ == "__main__":
    main()
