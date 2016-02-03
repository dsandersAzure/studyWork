from flask_restful import Resource
from flask import Response
from Bluetooth.Control \
    import global_control as global_control
from Bluetooth.Pairing_Control \
    import global_pair_control as pair_control_object
import json, requests

class Config_Output_Control(object):
    __controller = global_control
    __pair_controller = pair_control_object

    def __init__(self):
        pass


    def set_output(self, devicename=None, json_string=None):
        success = 'success'
        status = '200'
        message = 'Bluetooth output devices.'
        data = None

        try:
            if json_string == None\
            or json_string == '':
                raise KeyError('Badly formed request!')

            json_data = json.loads(json_string)
            key = json_data['key']
            output_item = json_data['output-item']
            file_name = json_data['file-name']

            if not key == '1234-5678-9012-3456':
                raise IndexError('Bluetooth key incorrect.')

            pairing_key = self.__pair_controller.check_pairing(devicename)

            if pairing_key == []:
                raise ValueError('Device is not paired')
            else:
                state = self.__pair_controller\
                    .add_output_device(devicename,
                                       output_item,
                                       'datavolume/'+devicename+'-'+file_name)
                print(state)
                data = {"device":devicename,
                        "output-item":output_item,
                        "file-name":'datavolume/'+devicename+'-'+file_name,
                        "state":"added" if state == True else "not added"}
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = str(ke)
        except ValueError as ve:
            success = 'error'
            status = '400'
            message = str(ve)
        except IndexError as ie:
            success = 'error'
            status = '403'
            message = str(ie)
        except Exception as e:
            raise

        return_value = self.__controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value


    def get_output(self, devicename):
        success = 'success'
        status = '200'
        message = 'Bluetooth output devices.'
        data = None

        try:
            pairing_key = self.__pair_controller.check_pairing(devicename)

            if pairing_key == []:
                raise ValueError('Device is not paired')
            else:

                data = {"outputs":
                    self.__pair_controller.get_output_devices(devicename)}
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Badly formed request!'
        except ValueError as ve:
            success = 'error'
            status = '400'
            message = str(ve)
        except IndexError as ie:
            success = 'error'
            status = '403'
            message = str(ie)
        except Exception as e:
            raise

        return_value = self.__controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value


    def delete_output(self, devicename=None, json_string=None):
        success = 'success'
        status = '200'
        message = 'Bluetooth output devices.'
        data = None

        try:
            if json_string == None\
            or json_string == '':
                raise KeyError('Badly formed request!')

            json_data = json.loads(json_string)
            key = json_data['key']
            output_item = json_data['output-item']

            if not key == '1234-5678-9012-3456':
                raise IndexError('Bluetooth key incorrect.')

            pairing_key = self.__pair_controller.check_pairing(devicename)

            if pairing_key == []:
                raise ValueError('Device is not paired')
            else:
                state = self.__pair_controller\
                    .remove_output_device(devicename, output_item)
                print(state)
                data = {"device":devicename,
                        "output-item":output_item,
                        "state":"deleted" if state == True else "not deleted"}
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = str(ke)
        except ValueError as ve:
            success = 'error'
            status = '400'
            message = str(ve)
        except IndexError as ie:
            success = 'error'
            status = '403'
            message = str(ie)
        except Exception as e:
            raise

        return_value = self.__controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value


config_output_control_object = Config_Output_Control()
