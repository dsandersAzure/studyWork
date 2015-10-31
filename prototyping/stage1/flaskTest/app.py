from flask import Flask, Blueprint, abort
from flask_restful import Api
import resources.Config as Config
from resources.HelloWorld import HelloWorld
from resources.Testing import Testing
from resources.HelloDavid import HelloDavid

app = Flask(__name__)
api = Api(app)

api.add_resource(HelloWorld, '/<string:message>', '/')
api.add_resource(Testing, '/testing')
api.add_resource(HelloDavid, '/David')

if __name__ == '__main__':
    app.run(debug=True)
