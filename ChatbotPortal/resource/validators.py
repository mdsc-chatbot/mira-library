from django.core.exceptions import ValidationError

# Validator for making sure that the file doesn't exceed a certain byte range
def validate_file_size(value):
    size = 50  # Size should be in mb range

    # Value size is in bytes
    # Reference: https://docs.djangoproject.com/en/2.2/ref/files/uploads/
    if value.size > size * (10 ** 6):
        raise ValidationError('Attachment is too large, file must be under {} MB'.format(size))