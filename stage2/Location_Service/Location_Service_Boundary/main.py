from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Location_Service import app, api
from Location_Service_Boundary import apiR
from Location_Service_Boundary.Check_Boundary import Check_Boundary

apiR.add_resource(Check_Boundary, '/v1_00/check')
