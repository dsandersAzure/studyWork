from Test import app, api
from Test.Control import global_controller
from Test_Config_Boundary.Config_Sample_Boundary \
    import Config_Sample_Boundary
from Test_Config_Boundary.Config_Logger_Boundary \
    import Config_Logger_Boundary
#
# Get the version of the API
#
version = global_controller.get_value('version')

api.add_resource(Config_Sample_Boundary,
                 '/{0}/config/sample'.format(version))
#
# Place config boundaries here
#
# End config boundaries here
#
api.add_resource(Config_Logger_Boundary,
                 '/{0}/config/logger'.format(version))

