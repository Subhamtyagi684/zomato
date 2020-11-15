from django.forms import ValidationError

def match_password(value):
    if value!='shubham':
        raise ValidationError('Password should only be shubham')
    return value