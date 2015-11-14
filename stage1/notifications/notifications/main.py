from flask_restful import Resource, Api
from notifications import app, api

import notifications.resources.Notifications as Notifications
#import notifications.resources.Notification_Schema as Notification_Schema
from notifications.resources.Notification_Schema import Notification_Schema
from notifications.resources.ma_Notification_Schema import Ma_Notification_Schema
import json
from pprint import pprint

#api.add_resource(Notifications, '/v1_01/notifications')
#api.add_resource(NotificationsID, '/v1_01/notifications/<int:id>')
##api.add_resource(NotificationAdder, '/notifications')
#api.add_resource(Lock, '/v1_01/lock')
#api.add_resource(Unlock, '/v1_01/unlock/<int:unlock_code>')
#api.add_resource(Helper, '/v1_01/', '/')
#api.add_resource(Modes, '/v1_01/modes/<int:mode>')
#api.add_resource(ModesGet, '/v1_01/modes')

notes = Notifications.Notification_List()
note = Notifications.Notification(note='Test notification', action='do something', sensitivity='low')
note.id = 1
notes.append(note)
note_schema = Notification_Schema()
ma_note_schema = Ma_Notification_Schema(many=True)
note_json = note_schema.dump(note)
text_note = json.loads('{"data": {"attributes": {"action":"Another action...","note": "Note number 2","sensitivity": "high"},"id": "-1","type":"Notification"}}')
load_schema = note_schema.loads(json.dumps(text_note))
new_note = Notifications.Notification(marshalled_data=load_schema)
new_note.id = 2
notes.append(new_note)
file = open('output.json','w')
print('Notifications in list is/are:')
file.write('{"data":'+str(ma_note_schema.dump([note, new_note]).data).replace("'", '"')+'}')
#for idx, n in notes.iter_items():
#    file.write(str(note_schema.dump(n).data).replace('\'', '"'))
#    json.dumps(n)
#    print('marshmallow-jsonapi')
#    pprint(note_schema.dump(n).data)
#    print()
#    print('marshmallow')
#    pprint(ma_note_schema.dump(n).data)
#    print()
file.close()
print()
 
