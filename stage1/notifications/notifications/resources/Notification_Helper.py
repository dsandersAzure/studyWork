from flask_restful import Resource, Api, reqparse, abort
from notifications import app, api

import notifications.resources.Config as Config
from notifications.resources.Notification_Lock import Notification_Lock
from notifications.resources.Notification_Schema import Notification_Schema
from notifications.resources.Response import Response_Object

class Notification_Helper(Resource):
    def get(self):
        ext_mode = False
        links = {'_links':{}}
        return_status = 200

        with app.test_request_context():
            links['_links']['self'] = {
                'identifier':0,
                'href':'http://'+Config.server_name+':'+str(Config.port_number)+\
                    api.url_for(Notification_Helper, _external=ext_mode),
                'rel':'links',
                'description':'Display routes supported by this service.',
                'methods':['GET','OPTIONS','HEAD']}

            links['_links']['notifications'] = {
                'identifier':1,
                'href':'http://'+Config.server_name+':'+str(Config.port_number)+\
                    api.url_for(Notification_Helper, _external=ext_mode)+\
                    'notifications/<string:controlkey>',
                'schema':'http://'+Config.server_name+':'+str(Config.port_number)+\
                    api.url_for(Notification_Schema, _external=ext_mode),
                'rel':'collection',
                'description':'Display and manipulate the notification list '+\
                    'and post new notifications.',
                'methods':['GET','POST', 'DELETE','OPTIONS','HEAD']}

            links['_links']['notifications_list'] = {
                'identifier':2,
                'href':'http://'+Config.server_name+':'+str(Config.port_number)+\
                    api.url_for(Notification_Helper, _external=ext_mode)+\
                    'notifications/<string:controlkey>/<int:identifier>',
                'rel':'notification',
                'schema':'http://'+Config.server_name+':'+str(Config.port_number)+\
                    api.url_for(Notification_Schema, _external=ext_mode),
                'description':'Edit, Delete, or Fetch individual notifications.',
                'methods':['GET','PUT', 'DELETE','OPTIONS','HEAD']}

            links['_links']['notifications_pair'] = {
                'identifier':3,
                'href':'http://'+Config.server_name+':'+str(Config.port_number)+\
                    api.url_for(Notification_Helper, _external=ext_mode)+\
                    'pair/<string:controlkey>',
                'rel':'notification',
                'schema':'http://'+Config.server_name+':'+str(Config.port_number)+\
                    api.url_for(Notification_Helper, _external=ext_mode)+'pair/schema',
                'description':'Pair with a Bluetooth device.',
                'methods':['GET','POST', 'DELETE','OPTIONS','HEAD']}

            links['_links']['lock'] = {
                'identifier':4,
                'href':'http://'+Config.server_name+':'+str(Config.port_number)+\
                    api.url_for(Notification_Lock, _external=ext_mode),
                'rel':'lock',
                'description':'Device lock',
                'methods':['GET','POST','OPTIONS','HEAD']}

            links['_links']['unlock'] = {
                'identifier':5,
                'href':'http://'+Config.server_name+':'+str(Config.port_number)+\
                    api.url_for(Notification_Lock, _external=ext_mode)+\
                    '?unlock_code=<int:unlock_code>',
                'rel':'lock',
                'description':'Device unlock',
                'methods':['PUT','OPTIONS','HEAD']}

        return Response_Object(links, return_status).response()


