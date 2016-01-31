#from flask_restful import Resource, Api, reqparse, abort
#from flask import Response
from Phone import app, api
#from Phone_Boundary import apiR
from Phone_Boundary.Location_Boundary import Location_Boundary
from Phone_Boundary.Lock_Boundary import Lock_Boundary
from Phone_Boundary.Unlock_Boundary import Unlock_Boundary
from Phone_Boundary.Notification_Boundary import Notification_Boundary

api.add_resource(Location_Boundary, '/v1_00/location')
api.add_resource(Lock_Boundary, '/v1_00/lock')
api.add_resource(Unlock_Boundary, '/v1_00/unlock')
api.add_resource(Notification_Boundary, '/v1_00/notification')
