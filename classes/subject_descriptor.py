from base_subject import BaseSubject


class SubjectDescriptor(object):

    def __init__(self, *args, **kwargs):
        self.value = None

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        if not isinstance(value, BaseSubject):
            raise TypeError('Subject must be an instance of BaseSubject.')
        self.value = value
