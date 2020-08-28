from re import ASCII

from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible


@deconstructible
class UsernameValidator(RegexValidator):
	flags = ASCII
	message = f'''
	This value cannot contains spaces nor uppercase letters,
	may contains alphanumeric, underscore or hyphen characters,
	must start with a letter or underscore and end with
	either a digit, a letter or underscore.
	'''.strip().replace('\n\t', ' ')
	regex = r'^[a-z_]([a-z\d_-]*[a-z\d_])?$'
