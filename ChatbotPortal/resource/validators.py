from django.core.validators import URLValidator, MaxValueValidator, MinValueValidator

# Model validators

def url_validation(value):
    validator = URLValidator()
    validator(value)

def rating_max_validation(value):
    validator = MaxValueValidator(5)
    validator(value)

def rating_min_validation(value):
    validator = MinValueValidator(1)
    validator(value)