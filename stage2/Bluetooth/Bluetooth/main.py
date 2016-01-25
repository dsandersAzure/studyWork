from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Bluetooth import app, api
from BluetoothBoundary.Versions_Boundary \
    import Versions_Boundary, Version_1_00_Boundary

api.add_resource(Versions_Boundary, '/')
api.add_resource(Version_1_00_Boundary, '/v1_00')