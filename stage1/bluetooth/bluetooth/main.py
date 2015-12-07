from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from bluetooth import app, api

import bluetooth.resources.Config as Config
from bluetooth.resources.Response import Response_Object

from jsonschema import validate, exceptions
import json
import sqlite3

class Bluetooth_Schema(Resource):
    def get(self):
        return_list = []
        return_status = 200
        return_success_fail = 'success'
        return_message = 'notification schema'
        try:
            f = open('schemas/bluetooth.json','r')
            schema = json.load(f)
            f.close()
            return_list = schema
        except Exception as e:
            return_status = 400
            return_success_fail = 'error'
            return_message = repr(e)

        return_dict = {return_success_fail:
            {"message":return_message,
             "status":return_status,
             "data":return_list
            }}

        return Response(
            json.dumps(return_dict),
            status=return_status,
            mimetype='application/json')

class Bluetooth_Helper(Resource):
    def get(self):
#        port_number = "5000"
        ext_mode = False
        links = {'_links':{}}
        return_status = 200

        with app.test_request_context():
            links['_links']['self'] = {
                'identifier':0,
                'href':'http://'+Config.server_name+':'+str(Config.port_number)+\
                    api.url_for(Bluetooth_Helper, _external=ext_mode),
                'rel':'links',
                'description':'Display routes supported by this service.',
                'methods':['GET','OPTIONS','HEAD']}

            links['_links']['bluetooth'] = {
                'identifier':1,
                'href':'http://'+Config.server_name+':'+str(Config.port_number)+\
                    api.url_for(Bluetooth_Helper, _external=ext_mode)+\
                    'bluetooth/<string:controlkey>/',
                'schema':'http://'+Config.server_name+':'+str(Config.port_number)+\
                    api.url_for(Bluetooth_Schema, _external=ext_mode),
                'rel':'collection',
                'description':'Display and manipulate the notification list '+\
                    'and post new bluetooth.',
                'methods':['POST','OPTIONS','HEAD']}

        return Response_Object(links, return_status).response()

class Say_Aloud(Resource):
    f = open('schemas/bluetooth.json','r')
    schema = json.load(f)
    f.close()

    def post(self, controlkey=None):
        if controlkey == None:
            return
        if not controlkey == Config.controlkey_master:
            return
        textToSay = None
        try:
            f = open('datavol/bluetooth_output.txt','a')
            textToSay = json.loads(reqparse.request.get_data().decode('utf-8'))
            validate(textToSay, self.schema)
            f.write('Read aloud: '+textToSay['message']+'\n')
            f.close()
            return Response(
                json.dumps({'Done it':'OK'}),
                status=200,
                mimetype='application/json')
        except Exception as e:
            return Response(
                json.dumps({'Done it':'BAD', 'error':repr(e)}),
                status=400,
                mimetype='application/json')
            print(repr(e))

api.add_resource(Say_Aloud,
                 '/v1_00/bluetooth/<string:controlkey>/')
api.add_resource(Bluetooth_Schema,
                 '/v1_00/bluetooth/schema/')
api.add_resource(Bluetooth_Helper,
                 '/v1_00/')
