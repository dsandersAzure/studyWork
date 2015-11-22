# Import marshmallow for light weight serialization & de-serialization
from marshmallow import Schema, fields, post_load, post_dump

# Import jsonschema for Schema validation
from jsonschema import validate, exceptions

# Import JSON for JavaScript Object Notation serialization
import json

class Notifications(object):
    def __init__(self):
        self.__iter_index = 0
        self.__notification_list = []

    def push(self
            ,note=None
            ,action=None
            ,sensitivity=None):
        self.__notification_list.append(Notification(note,action,sensitivity))
        note_list = len(self.__notification_list)
        if note_list > 1:
            self.__notification_list[-1].identifier = \
                self.__notification_list[-2].identifier + 1
        elif note_list == 1:
            self.__notification_list[-1].identifier = 1
        return self.__notification_list[-1].identifier

    def pop(self):
        if len(self.__notification_list) < 1:
            raise IndexError('pop from empty list')
        del(self.__notification_list[:1])

    def dump(self):
        __schema__ = Notification.Notification_Schema(many=True)
        return str(__schema__.dump(self.__notification_list).data)\
            .replace("'",'"')

    def load(self, json_data=None):
        self.__notification_list = []
        error_count = 0
        error_text = ''

        if json_data == None:
            raise SyntaxError('JSON data must be passed to load as a list')
        __schema__ = Notification.Notification_Schema(many=True)
        for note in json_data:
            try:
                new_id = self.push()
                note_to_load = str(note).replace("'",'"')
                self.__notification_list[self.index(new_id)].load(note_to_load)
            except exceptions.ValidationError as ve:
                error_count += 1
                error_text += 'Error ' + str(error_count) + ':' + \
                    ve.message + '\n'
                del(self.__notification_list[self.index(new_id)])
        if error_count > 0:
            error_text = '\n\n\033[1m\033[4m' + \
                'Warnings occurred during data loading.\033[0m\n\n' +\
                error_text
            raise exceptions.ValidationError(error_text)

    def __len__(self):
        return len(self.__notification_list)

    def __iter__(self):
        for note in self.__notification_list:
            yield note

    def index(self, index):
        if not type(index) == int:
            raise TypeError('{0} is not a number. Index must be a number'\
                .format(index))
        for idx, note in enumerate(self.__notification_list):
            if note.identifier == index:
                return idx
        raise ValueError('{0} is not in list.'.format(index))

    def __getitem__(self, index):
        if not type(index) == int:
            raise TypeError('{0} is not a number. Index must be a number'\
                .format(index))
        if index > self.__notification_list[-1].identifier \
        or index < self.__notification_list[0].identifier:
            raise IndexError('Notification {0} does not exist.'\
                .format(index))
        try:
            index_position = self.index(index)
        except ValueError as v:
            raise IndexError('Notification {0} does not exist.'\
                .format(index))
        return self.__notification_list[index_position]

class Notification(object):

    # Define the schema as a class level variable
    file_handle = open('schemas/Notification_Schema.json', 'r')
    __schema__ = json.load(file_handle)
    file_handle.close()

    # Define the Marshmallow shcema
    class Notification_Schema(Schema):
        note = fields.String(required=True)
        action = fields.String(required=True)
        sensitivity = fields.String(required=False)
        identifier = fields.Integer(dump_only=True)

        @post_dump()
        def wrapper(self, data):
            return { 'notification' : data }

    # Class initializer
    def __init__(self
                ,note=None
                ,action=None
                ,sensitivity=None):
        self.identifier = -1
        self.related_links = []
        self.note = note
        self.action = action
        self.sensitivity = sensitivity

    # Class representation when used with repr(x) or str(x)
    def __repr__(self):
        return 'Notification(<identifier={self.identifier!r}>)'.format(self=self)

    # Class representation as a string when used with str(x)
    def __str__(self):
        return_string = 'Notification '+str(self.identifier)+'; '
        return_string += 'note: '+ (self.note or 'None') + ', '
        return_string += 'action: '+ (self.action or 'None') + ', '
        return_string += 'sensitivity: '+ (self.sensitivity or 'None') + ', '
        return return_string

    def dump(self):
        data_string = None
        return_string = None

        # Create a private instance of the schema
        __n_schema = self.Notification_Schema(many=False)

        # create the serialized data in JSON using the schema
        # note, for json.loads to work successfully, the ' characters in 
        # the schema output are replaced with "
        #
        data_string = str(__n_schema.dump(self).data).replace('None','null')
        return_string = data_string.replace("'",'"')

        return return_string

    def load(self, json_data, strict=False):
        current_step = 0
        try:
            # Load the provided JSON string into a dict
            __json_data = json.loads(json_data)
            current_step += 1

            # Step 1 - Validate the JSON data against the schema
#            validate(__json_data['notification'], self.__schema__)
            validate(__json_data, self.__schema__)
            current_step += 1

            # Step 2 - Use marshmallow to deserialize
            __n_schema = self.Notification_Schema(many=False, strict=False)
            __result = __n_schema.load(__json_data['notification']).data
            current_step += 1

            # Step 3 - Update this object to the values loaded from JSON data.
            #          Note that the ID is ignored.
            if 'note' in __result:
                self.note = __result['note']

            if 'action' in __result:
                self.action = __result['action']

            current_step += 1
            if 'sensitivity' in __result:
                self.sensitivity = __result['sensitivity']
        except exceptions.ValidationError as v:
            exception_string = 'There is invalid data within the JSON data:'
            exception_string += ' "\033[1m' + v.message + '"\033[0m\n'
            exception_string += ' >> ' 
            exception_string += str(__json_data['notification']) + '\n'
            exception_string += 'The following fields are required and '
            exception_string += 'may not be null or None: '
            required_fields = self.__schema__['properties']['notification']['required']
#['properties']\
#                ['notifications']['required']
            for idx2, key in enumerate(required_fields):
                exception_string += '\033[4m'
                exception_string += required_fields[idx2]
                exception_string += '\033[0m '
            exception_string += '\n'
            raise exceptions.ValidationError(exception_string)
        except Exception as e:
            print('An unknown exception occured at {1}: {0}'\
                  .format(str(e), current_step))

        return

    def iter_fields(self):
        yield "ID", self.identifier
        yield "note", self.note
        yield "action", self.action
        yield "sensitivity", self.sensitivity

