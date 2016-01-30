from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Location_Service \
    import app, api, control, \
           check_control

from Location_Service_Boundary import apiR

class Check_Boundary(Resource):
    def get(self):
        raw_data = None
        raw_data = reqparse.request.get_data().decode('utf-8')
        return_state = check_control.check(json_string=raw_data)

        return return_state

