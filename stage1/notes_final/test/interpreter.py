# Import 
# Reference: 
# Argparse Tutorial - https://docs.python.org/2/howto/argparse.html#id1
#
# Import argpars to parse command line arguments
import argparse

# Import requests, sys, json, and pprint for http methods and formatting #
import requests
import sys
import json
from pprint import pprint

# Import Marshmallow for schema loading #
from marshmallow import Schema, fields, post_load

# Global variables
interactive = False
g_links = []

# Class definitions
class Link(object):
    def __init__(self, description=None, href=None, rel=None):
        self.headers = []
        self.identifier = -1
        self.description = description
        self.href = href
        self.rel = rel
        self.parameters = []

    def __repr__(self):
        return '<Link(identifier={self.identifier!r}>'.format(self=self)

    def to_string(self):
        return str(self.identifier) + ' ' + \
               self.description + ' (' + \
               self.href + ') '

    def get_headers(self):
        result = requests.options(self.href)
        if result.status_code == 200:
            self.headers = result.headers

# Schema definition for Marshmallow
class LinkSchema(Schema):
    description = fields.Str(required=True)
    href = fields.Url(required=False)
    rel = fields.Str(required=True)

    @post_load
    def make_link(self, data):
        return Link(**data)

def fetch_routes(server_name):
    try:
        global g_links
        result = requests.get(server_name)
        if '_links' in result.json():
            _links = result.json()['_links']
            g_links = LinkSchema(many=True, strict=False).load(_links).data
            if not g_links == None:
                print()
                for index, link in enumerate(g_links):
                    link.identifier = index
                    link.get_headers()
                    print('{0:2d} {1:30s} {2:40s} {3:s}'.format(
                        index
                       ,link.description
                       ,link.href
                       ,link.headers['allow']
                    ))
                print()
        else:
            raise ValueError('No links were found at the root address:')
    except ValueError as e:
        print('{0} {1}'.format(e, server_name))
    except Exception as e:
        print()
        print('error. '+repr(e))

def fetch_route(command):
    try:
        args = command.split()
        if len(args) < 2:
            raise ValueError('correct usage: route <route>, where <route> '+\
                             'is a number.')
    except ValueError as e:
        print(e)
    except Exception as e:
        print()
        print('error. '+repr(e))

def header(command):
    try:
        args = command.split()
        if len(args) < 2 or len(args) > 2:
            raise Exception('correct usage: '+args[0]+' <route>, where <route> '+\
                             'is a number.')

        route = int(args[1])
        if route < 0:
            raise ValueError("The route cannot be less than zero.")
        elif route > len(g_links):
            raise IndexError("The route doesn't exist. Have you run routes?")

        print()
        headers = g_links[route].headers
        for header_item in headers:
            print('{0:20s} {1}'.format(header_item, headers[header_item]))
        print()
    except Exception as e:
        print('error. '+str(e))

def get(command):
    try:
        args = command.split()
        if len(args) < 2:
            raise Exception('correct usage: get <route>, where <route> '+\
                             'is a number.')

        content_to_find = None
        if len(args) > 2:
            content_to_find = str(args[2])

        route = int(args[1])
        if route < 0:
            raise ValueError("The route cannot be less than zero.")
        elif route > len(g_links):
            raise IndexError("The route doesn't exist. Have you run routes?")
        if not 'GET' in g_links[route].headers['allow']:
            raise Exception('HTTP 405 - This route does not support GET')

        result = requests.get(g_links[route].href)
        if not result.status_code == 200:
            raise Exception('HTTP {0}'.format(result.status_code))
        elif not 'json' in result.headers['content-type']:
            raise Exception('Expected JSON data but did not receive it.')

        print()
        headers = result.headers
        for header_item in headers:
            print('{0:20s} {1}'.format(header_item, headers[header_item]))
        print()

        data_set = result.json()
        data_keys = data_set.keys()

        if not content_to_find == None:
            if not content_to_find in data_set:
                key_string = ""
                for key in data_set.keys():
                    key_string = key_string + key + ','
                raise Exception('Content "'+content_to_find+ \
                                '" does not exist. Possible choices are '+ \
                                'one of: [' + \
                                key_string + ']')
            if type(data_set[content_to_find]) is dict:
                print('Data')
                print('-'*80)
                for key in data_set[content_to_find]:
                    if key != '_links':
                        print('{0:30s}: {1}' \
                              .format(key, data_set[content_to_find][key]))
                print()
                print('Links')
                print('-'*80)
                for key in data_set[content_to_find]['_links']:
                    print('{0:30s}: {1}'.format(key, data_set[content_to_find]['_links'][key]))
            else:
                pprint(data_set)
        else:
            print('Keys')
            print('-'*80)
            for key in data_keys:
               print('{0}'.format(key))
        print()

    except Exception as e:
        print('error. '+str(e))

def help(server):
    print()
    print('options')
    print()
    print('help - execute this command')
    print('routes - list all routes available from root server {0}' \
          .format(server))
    print('get <route> - get (curl -X GET) the route identified '+ \
          'by <route> returning keys in dictionary items, otherwise ' +\
          'the values.')
    print('get <route> <key> - get (curl -X GET) the route identified '+\
          'by <route> and <key>')
    print('put <route> <key> - put (curl -X PUT) the route identified by <route>')
    print('post <route> - post (curl -X POST) the route identified by <route>')
    print('delete <route> - post (curl -X DELETE) the route '+\
          'identified by <route>')
    print('head <route> - show the header and options for <route>')
    print()

try:
    parser = argparse.ArgumentParser()
    parser.add_argument("server"
                       ,type=str
                       ,help="Fully qualified url for the device"+\
                             ", e.g. http://localhost:82/ **NOTE** "+\
                             "the port and closing / should be provided")
    args = parser.parse_args()
    if args.server:
        server = args.server

    while True:
        command = input(server + ' > ')
        if command.upper()[:4] == 'EXIT':
            break
        elif command.upper()[:6] == 'ROUTES':
            fetch_routes(server)
        elif command.upper()[:6] == 'ROUTE ':
            fetch_route(server)
        elif command.upper()[:7] == 'HEADER ' \
        or   command.upper()[:5] == 'HEAD ' \
        or   command.upper()[:8] == 'OPTIONS ':
            header(command)
        elif command.upper()[:4] == 'GET ':
            get(command)
        elif command.upper()[:5] == 'HELP ' \
        or   command.upper()[:4] == 'HELP'  \
        or   command.upper()[:1] == '?':
            help(server)
        elif command == '':
            pass
        else:
            print('Unknown command [{0}]'.format(command))
except EOFError as e:
    print()
except Exception as e:
    raise e


