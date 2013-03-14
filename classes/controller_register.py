from bhp_dispatch.exceptions import AlreadyRegisteredController


class ControllerRegister(object):
    """Registers controllers to prevent more than one controller instance for the same settings_key."""
    def __init__(self):
        self._register = []

    def register(self, controller):
        from base_controller import BaseController
        if not isinstance(controller, BaseController):
            raise TypeError('Controller must be an instance of bhp_dispatch.classes.Base.')
        if str(controller) in self._register:
            raise AlreadyRegisteredController('{0} has already been registered.'.format(str(controller)))
        self._register.append(str(controller))

    def deregister(self, controller):
        try:
            self._register.remove(str(controller))
        except:
            pass

registered_controllers = ControllerRegister()
