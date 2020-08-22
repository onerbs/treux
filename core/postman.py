from django.core.mail import send_mail
from django.template.loader import get_template
from django.utils.html import strip_tags
from faker import Faker

from treux.settings import SITE_URL

fake = Faker()


def send_confirmation_email(user):
	subject = 'Please, confirm your postman'
	html = _render_template(
		subject, 'confirm', user.uuid,
		'confirmation', {
			'headline': 'Welcome,' + user.get_short_name(),
		}
	)
	if _send_email(subject, user.email, html) > 0:
		user.mail_sent = True
		user.save()


def send_reset_pass_email(user) -> int:
	subject = 'Reset your password'
	html = _render_template(
		subject, 'reset', user.uuid,
		'reset_pass', {
			'headline': 'Hi,' + user.get_short_name(),
		}
	)
	return _send_email(subject, user.email, html)


def _render_template(
		subject: str, action: str, uuid: str,
		template: str, context: dict = None) -> str:
	context = {
		**context,
		'link_color': fake.color(),  # '#d23049',
		'phone_number': fake.phone_number(),
		'subject': subject,
		'url': f'{SITE_URL}/{action}/?u={uuid}',
	}
	return str(get_template(f'postman/{template}.html').render(context))


def _send_email(subject: str, email: str, html: str) -> int:
	return send_mail(
		subject, strip_tags(html), None, [email], html_message=html)
