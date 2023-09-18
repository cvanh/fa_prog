from clint.textui import validators

# this function is bases on the implemtation in : https://github.com/kennethreitz-archive/clint/blob/master/clint/textui/validators.py#L58
# this is an helper to verify that the pincode that is entered is 4 charachters long
class check_pincode(object):
    message = 'your code is too short or contains ;'

    def __init__(self, message=None):
        if message is not None:
            self.message = message

    def __call__(self, value):
        # check if pincode is 4 charachters and does not contain a ; 
        if (len(value) != 4) | (";" in value):
            raise validators.ValidationError(self.message)
        return value