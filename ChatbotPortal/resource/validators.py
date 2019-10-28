from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Validator for making sure that the file doesn't exceed a certain byte range
# Size should be in mb range
def validate_file_size(size=50):

    def internal_validator(value):
        # Value size is in bytes
        # Reference: https://docs.djangoproject.com/en/2.2/ref/files/uploads/
        if value.size > size * (10 ** 6):
            raise ValidationError('Attachment is too large, file must be under {} MB'.format(size))

    return internal_validator