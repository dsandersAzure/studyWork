from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Phone import app, api, control, lock_control_object
from Phone_Boundary import apiR

class Lock_Boundary(Resource):
    def get(self):
        return lock_control_object.is_locked()
#        print('LOCK GET')
#        return_value = pair_control_object.pair_info(devicename)
#        return return_value


    def post(self):
        return lock_control_object.lock_request()

