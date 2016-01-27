from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Phone.Phone_Database import Phone_Database

import datetime, time, json

#
# SuperClass.
# ----------------------------------------------------------------------------
class Control(object):
    __log_file = 'datavolume/Log_File.txt'
    __phone_db = None

    def __init__(self):
        self.__phone_db = Phone_Database()


    def persist_notification(
        self,
        sender=None,
        date_string=None,
        notification=None,
        action=None
    ):
        self.__phone_db.save_notification(
            sender,
            date_string,
            notification,
            action
        )


    def get_bluetooth(self):
        return self.__phone_db.get_bluetooth_device()


    def log(self,
            log_message=None
    ):
        now = datetime.datetime.now()
        f = None
        try:
            f = open(self.__log_file, 'a')
            f.write('{0}: {1}'.format(now,log_message)+"\n")
        except Exception:
            raise
        finally:
            if not f == None:
                f.close()

    def do_response(self,
                    status=200,
                    response='success',
                    data=None,
                    message=''):
        return_dict = {"status":status,
                       "response":response,
                       "data":data,
                       "message":message}
        return Response(
            json.dumps(return_dict),
            status=status,
            mimetype='application/json')


#
# Version 1.00
# ----------------------------------------------------------------------------
class Control_v1_00(Control):
    def future(self):
        pass

