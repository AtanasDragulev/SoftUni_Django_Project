from django.core.exceptions import ValidationError


def validate_category_not_self(value):
    pass


def validate_characters_only(value):
    if not value.isalpha():
        raise ValidationError("Field can only contain characters (letters).")


def validate_characters_digits_only(value):
    if not all((x.isalpha() or x.isspace() or x.isdigit()) for x in value):
        raise ValidationError("Field can only contain characters, numbers and spaces.")


def validate_characters_digits_dashes_only(value):
    if not all((x.isalpha() or x == '-' or x.isdigit()) for x in value):
        raise ValidationError("Field can only contain characters, numbers and dashes '-'.")


def validate_numbers_plus_sign_only(value):
    if not all((x.isdigit()) or x.isspace() or x == "+" for x in value):
        raise ValidationError('Field can only contain numbers, spaces and the "+" sing.')


MAX_SIZE_IN_MB = 10


def validate_image_size(value):
    max_size = MAX_SIZE_IN_MB * 1024 * 1024

    if value.size > max_size:
        raise ValidationError(f"Image size should not exceed {MAX_SIZE_IN_MB} MB.")
