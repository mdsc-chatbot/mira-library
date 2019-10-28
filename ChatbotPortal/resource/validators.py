from django.core.exceptions import ValidationError

#TODO: actually validate the file size here
# Validator for making sure that the file doesn't exceed a certain byte range
# Size should be in mb range
def validate_file_size(size=100):

    def internal_validator(value):
        pass

    return internal_validator