"""
    Module:      __init__.py
    Overivew:    The initialization module of the package notes.
    Purpose:     Define the app and api variables.
                 Import the main.py main module.
    Patterns:    Larger Applications pattern from Flask website (Ronacher,
                 2013)

    References
    ----------
    Ronacher, A., 2013, 'Larger Applications' [ONLINE]. Available at: 
    http://flask.pocoo.org/docs/0.10/patterns/packages/ (Accessed: 04 November 
    2015)

"""
# Import the module Flask from the flask package
from flask import Flask

# Import the module Api from the flask_restful package
from flask_restful import Api

# Import PairControl
from Phone import Control
#from Phone import Broadcast_Control
from Phone import Notification_Control

# The app is this application and set when the Python file is run from the
# command line, e.g. python3 /some/folder/notes/runserver.py
app = Flask(__name__)
# Create an Api object inheriting app
api = Api(app)

#Setup objects for pairing and broadcasting.
notification_control_object = Notification_Control.Notification_Control_v1_00()
#broadcast_control_object = Broadcast_Control.Broadcast_Control_v1_00()
control = Control.Control_v1_00()

# Import the main.py module
import Phone.main

