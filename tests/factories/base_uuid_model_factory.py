from bhp_factory.factories import BaseFactory

starting_seq_num = 0


class BaseUuidModelFactory(BaseFactory):
    ABSTRACT_FACTORY = True

    @classmethod
    def _setup_next_sequence(cls):
        return starting_seq_num
