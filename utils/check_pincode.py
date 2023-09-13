from clint.textui import validators

# this is an helper to verify that the pincode that is entered is 4 charachters long
class check_pincode(object):
    message = 'your code is too short or contains ;'

    def __init__(self, message=None):
        if message is not None:
            self.message = message

    def __call__(self, value):
        # check if picode 
        if len(object) == 4 | ";" in object:
            raise validators.ValidationError(self.message)
        return value