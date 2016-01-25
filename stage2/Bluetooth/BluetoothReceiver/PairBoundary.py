from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Bluetooth import app, pair_control_object
from BluetoothReceiver import apiR

class PairBoundary(Resource):
    def get(self, devicename):
        return pair_control_object.pair_info(devicename)

    def post(self, devicename):
        return pair_control_object.pair_device(devicename)

    def delete(self, devicename):
        return pair_control_object.pair_unpair(devicename)


