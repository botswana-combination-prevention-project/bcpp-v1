import factory


class BaseFactory(factory.DjangoModelFactory):
    ABSTRACT_FACTORY = True
