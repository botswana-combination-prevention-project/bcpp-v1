from base_rule import BaseRule


class Rule(BaseRule):

    def __init__(self, *args, **kwargs):

        self._predicate = None
        self._consequent_action = None
        self._alternative_action = None
        super(Rule, self).__init__(*args, **kwargs)

    def set_consequent_action(self):
        self._consequent_action = self.logic.consequence

    def get_consequent_action(self):
        self.set_consequent_action()
        return self._consequent_action

    def set_alternative_action(self):
        self._alternative_action = self.logic.alternative

    def get_alternative_action(self):
        self.set_alternative_action()
        return self._alternative_action

    def set_predicate(self):
        self._predicate = None
        source_model_instance = self.get_source_model_instance()
        if source_model_instance:
            self._predicate = ''
            unresolved_predicate = self.logic.predicate
            if isinstance(unresolved_predicate[0], basestring):
                unresolved_predicate = (unresolved_predicate,)
            # build the predicate
            # check that unresolved predicate is a tuple
            if not isinstance(unresolved_predicate, tuple):
                raise TypeError('First \'logic\' item must be a tuple of (field, operator, value). Got %s' % (unresolved_predicate,))
            n = 0
            for item in unresolved_predicate:
                if n == 0 and not len(item) == 3:
                    ValueError('The logic tuple (or the first tuple of tuples) must must have three items')
                if n > 0 and not len(item) == 4:
                    ValueError('Additional tuples in the logic tuple must have a boolean operator as the fourth item')
                field_value = getattr(source_model_instance, item[0])
                # comparison value
                value = item[2]
                # boolean operator if more than one tuple in the logic tuple
                if len(item) == 4:
                    boolean_operator = item[3]
                    if boolean_operator not in ['and', 'or', 'and not', 'or not']:
                        ValueError('Illegal operator in logic tuple for rule %s' % (self))
                else:
                    boolean_operator = ''
                # add as string for eval
                self._predicate += ' %s (\'%s\' == \'%s\')' % (boolean_operator, field_value.lower(), value.lower())
                n += 1

    def get_predicate(self):
        """Gets the predicate, but return value may be '' or None, so users should check for this."""
        # always set
        self.set_predicate()
        return self._predicate
