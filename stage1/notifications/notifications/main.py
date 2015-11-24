from flask_restful import Resource, Api, reqparse, abort
from notifications import app, api

from notifications.resources.Notifications import Notification
from jsonschema import validate, exceptions
import json
import sqlite3

class Notification_Boundary_All(Resource):
    def get(self):
        try:
            return_list = []
            return_string = ''

            db_connection = sqlite3.connect('datavol/notifications.db')
            db_cursor = db_connection.cursor()
            db_cursor.execute(
                'select key, value from notifications'
            )
            db_records = db_cursor.fetchall()
            for db_row in db_records:
                note = Notification()
                note.load(db_row[1])
                if not note.sensitivity == 'high':
                    return_list.append(note.dump())
                    return_string += ' '+note.dump()
        except exceptions.ValidationError as ve:
            pass
        except Exception as e:
            return {'error':repr(e)}
        finally:
             db_cursor.close()
             db_connection.close()
        
        return return_list

    def post(self):
        return_list = []
        return_status = 201
        database_opened = False
        updated_data = False

        try:
            raw_json = reqparse.request.get_data().decode('utf-8')
#            json_data = json.loads(raw_json)
            note = Notification()
            note.load(raw_json)

            db_connection = sqlite3.connect('datavol/notifications.db')
            db_cursor = db_connection.cursor()
            db_cursor.execute( \
                'insert into notifications '+ \
                'values (?, ?)', \
                (note.identifier, raw_json) \
            )
            db_connection.commit()
            return_list = str(note)
        except IndexError:
            abort(404)
        except exceptions.ValidationError as ve:
            return_status = 400
            return_list = {'error':'Data not loaded. '+\
                str(ve.message), 'status':return_status}
        except Exception as e:
            return_status = 400
            return_list = {'error':repr(e), 'status':return_status}
        finally:
            if database_opened:
                db_cursor.close()
                db_connection.close()

        return return_list

class Notification_Boundary_One(Resource):
    def get(self, id):
        return 'Hello World {0}'.format(id)


api.add_resource(Notification_Boundary_All, '/v1_00/notifications')
api.add_resource(Notification_Boundary_One, '/v1_00/notifications/<int:id>')

