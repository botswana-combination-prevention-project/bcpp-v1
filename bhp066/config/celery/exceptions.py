
class CeleryTaskAlreadyRunning(Exception):
    pass


class CeleryNotRunning(Exception):
    pass


class CeleryTaskFailed(Exception):
    pass
