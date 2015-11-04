#from app import api
from flask_restful import Resource, request, reqparse
from flask import abort, url_for
import resources.Config as Config
import sys

class Notifications(Resource):
    def get(self):
        returnList = []
#        with app.test_request_context():
        for idx, note in enumerate(Config.notificationList):
            from app import api
            temp_dict = {'note':note['note']}
            if not Config.locked:
                temp_dict['_link'] = api.url_for(NotificationGetter, id = idx)
#                temp_dict['_link'] = str(url_for(NotificationGetter, id=idx))
            returnList.append(temp_dict)
        
        return {'notifications':returnList}

class NotificationGetter(Resource):
    def get(self, id):
        try:
            if Config.locked:
                return {'notice':'unlock device first'}
            return Config.notificationList[id]
        except IndexError:
            abort(404)
        except:
            return {'error':str(sys.exc_info()[0])}

    def put(self, id):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('note', type=str)
            parser.add_argument('action', type=str)
            args = parser.parse_args()

            for k, v in args.items():
                if k.upper() in ['NOTE','ACTION'] \
                and not v == None:
                    Config.notificationList[id][k] = v

            return(Config.notificationList[id])
        except IndexError:
            abort(404)
        except:
            return {'error':str(sys.exc_info()[0])}

class NotificationAdder(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument(
                'note',
                type=str,
                required=True,
                help='You must provide a message for the notification'
            )
            parser.add_argument(
                'action',
                type=str,
                required=True,
                help='You must provide an action'
            )
            args = parser.parse_args()

            Config.notificationList.append({
                    'note':args['note'],
                    'action':args['action']
                }
            )
            return {'notification sent':Config.notificationList[-1:]}
        except:
            return {'error':str(sys.exc_info()[0])}
