from django.template.loader import get_template
from faker import Faker

from core.postman.tasks import send_email
from treux.api import api_url


def send_confirmation_email(user):
	subject = 'Please, confirm your email'
	html = _render_template(
		subject, user.uuid, 'confirm%ation', {
			'headline': 'Welcome, ' + user.get_short_name(),
		}
	)
	send_email.apply_async(args=[subject, user.email, html])


def send_reset_pass_email(user):
	subject = 'Reset your password'
	html = _render_template(
		subject, user.uuid, 'reset%_pass', {
			'headline': 'Hi, ' + user.get_short_name(),
		}
	)
	send_email.apply_async(args=[subject, user.email, html])


def _render_template(
		subject: str, uuid: str, res: str, context: dict = None) -> str:
	action, template = res.split('%')[0], res.replace('%', '')
	context = {
		**context,
		'link_color': '#d23049',
		'phone_number': Faker(['jp_JP']).phone_number(),
		'subject': subject,
		'url': api_url(f'{action}/?u={uuid}'),
	}
	return str(get_template(f'postman/{template}.html').render(context))
