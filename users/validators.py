from re import ASCII

from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible


@deconstructible
class UsernameValidator(RegexValidator):
	flags = ASCII
	message = \
		'This value may contain only English letters, ' \
		'numbers, and [._-] characters.'
	regex = r'^[a-zA-Z0-9\._-]+$'
