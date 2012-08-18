

class Coder(object):

    """Encode / Decode base36 """
    def encode(self, number=None, has_check_digit=False, alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'):

        """Convert positive integer to a base36 string."""
        # access internally as encode()
        # access and pass a number to encode, check_digit not part of the number
        # access and pass a number to encode, which includes a check_digit
        # always add check_digit (or add it back) before encoding
        if number:
            self.identifier_string = number
            # is last digit a check digit?
            if has_check_digit:
                # ok, but is it valid
                if self.is_valid(number, False):
                    # yes,
                    self.identifier_string = self.identifier_string[0:-1]
                else:
                    # no
                    raise ValueError('Invalid identifier. Last digit should be %s which is the modulus %s of %s, Got %s' % (int(str(number)[0:-1]) % self.modulus, self.modulus, str(number)[0:-1], str(number)[-1]))
        # we don't store the check_digit as part of the identifier_string, so add it back
        number = int(self.identifier_string + str(self.check_digit()))
        if not isinstance(number, (int, long)):
            raise TypeError('number must be an integer')
        # Special case for zero
        if number == 0:
            return alphabet[0]
        base36 = ''
        sign = ''
        if number < 0:
            sign = '-'
            number = -number
        while number != 0:
            number, i = divmod(number, len(alphabet))
            base36 = alphabet[i] + base36
        self.identifier = sign + base36
        return self.identifier

    def decode(self, base36=None, has_check_digit=False):

        if base36:
            self.has_check_digit = has_check_digit
            self.identifier = base36
        decoded_number = str(int(self.identifier, 36))
        if self.has_check_digit:
            # assume last digit is the check digit
            if int(decoded_number[0:-1]) % self.modulus == int(decoded_number[-1]):
                self.identifier_string = decoded_number[0:-1]
            else:
                raise ValueError('Invalid identifier. Last digit should be %s which is the modulus %s of %s, Got %s' % (decoded_number[0:-1] % self.modulus, self.modulus, decoded_number[0:-1], decoded_number[-1]))
        else:
            self.identifier_string = decoded_number
        return self.identifier_string
