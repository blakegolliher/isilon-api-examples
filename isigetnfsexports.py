#!/usr/bin/python
##
# Simple report on nfs exports
# on Isilon 7.0 and above.
##
# blake golliher
# blakegolliher@gmail.com
#
##

import urllib2, os, base64, getpass, sys
import simplejson as json

usage = """
EXAMPLE

isigetnfsexports.py clustername

"""

if len(sys.argv)!=2:
    print (usage)
    sys.exit(0)

clustername = sys.argv[1]

password = getpass.getpass()

request = urllib2.Request("https://" + clustername + ":8080/platform/1/protocols/nfs/exports")
request.add_header('Accept', 'application/json')
base64string = base64.encodestring('%s:%s' % ('root',password)).replace('\n', '')
request.add_header("Authorization", "Basic %s" % base64string)
result = urllib2.urlopen(request)

data = json.load(result)

ids = []
paths = []
clients = []
root_clients = []
read_write_clients = []

for item in data['exports']:
	ids.append(item['id'])
        paths.append(item['paths'])
        clients.append(item['clients'])
        root_clients.append(item['root_clients'])
        read_write_clients.append(item['read_write_clients'])

for id,path,clients,rclients,rwclients in zip(ids, paths, clients, root_clients, read_write_clients):
        print "Export ID 		: %s " % id
	print "Path Exported		: %s " % path
        print "  Clients 		: %s " % clients
        print "  Root Clients 		: %s " % rclients
        print "  Read Write Clients 	: %s \n" % rwclients
