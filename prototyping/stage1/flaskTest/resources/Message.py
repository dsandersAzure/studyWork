from flask_restful import Resource, reqparse
from flask import Flask, abort
import resources.Config as Config
import sqlite3

class Message(Resource):
    def get(self, key):
        try:
            return Config.message[key]
        except:
            abort(404)

    def put(self, key):
        parser = reqparse.RequestParser()
        parser.add_argument('data')
        args = parser.parse_args()

        try:
            Config.message[key] = args['data'] 
            return Config.message[key]
        except:
            abort(400)

    def delete(self, key):
        try:
            del(Config.message[key])
            return {'delete':'Key ['+key+'] deleted.'}
        except:
            abort(404)

class Messages(Resource):
    def get(self):
        return Config.message

class MessageSpecific(Resource):
    def get(self, identifier, key):
        try:
            verified_identities = []
            connection = sqlite3.connect(Config.database_connection)
            cursor = connection.cursor()
            cursor.execute(
               'select identifier from identities where identifier = ?',
               (identifier,)
            )
            while True:
                row = cursor.fetchone()
                if row == None:
                    break
                verified_identities.append(row[0])
            if len(verified_identities) < 1:
                cursor.close()
                connection.close()
                return(
                    {
                     'error':'unauthorized'
                    })
            else:
                return(
                {
                     'action':'get user specific message',
                     'for':identifier,
                     'key':key,
                     'message':Config.message[key],
                     'verified':verified_identities
                })
            cursor.close()
            connection.close()
        except:
            cursor.close()
            connection.close()
            abort(400)
