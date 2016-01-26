from flask_restful import Resource, Api, reqparse, abort
from flask import Response

import datetime, time, json

#
# SuperClass.
# ----------------------------------------------------------------------------
class Control(object):
    __log_file = 'datavolume/Log_File.txt'


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

