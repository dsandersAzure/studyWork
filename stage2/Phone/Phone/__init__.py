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

# Import werkzueg
from werkzeug import serving

# Import PairControl
from Phone import Control
#from Phone import Broadcast_Control
from Phone import Notification_Control
from Phone import Location_Control
from Phone import Lock_Control

# The app is this application and set when the Python file is run from the
# command line, e.g. python3 /some/folder/notes/runserver.py
app = Flask(__name__)
# Create an Api object inheriting app
api = Api(app)

#if not serving.is_running_from_reloader():
try:
    #Setup objects for pairing and broadcasting.
    notification_control_object = Notification_Control.Notification_Control_v1_00()
    location_control_object = Location_Control.Location_Control_v1_00()
    lock_control_object = Lock_Control.Lock_Control_v1_00()
    control = Control.Control_v1_00()
except KeyError as ke:
    print(ke)

# Import the main.py module
import Phone.main
