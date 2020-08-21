from django.core.mail import send_mail
from django.template.loader import get_template
from django.utils.html import strip_tags
from faker import Faker

from treux.settings import SITE_URL

fake = Faker()


def send_confirmation_email(user):
	subject = 'Please, confirm your postman'
	url = f'{SITE_URL}/confirm/?u={user.uuid}'
	html = _render_template('confirmation', {
		'headline': 'Welcome,' + user.get_short_name(),
		'subject': subject,
		'url': url,
	})
	if _send_email(subject, user.email, html) > 0:
		user.mail_sent = True
		user.save()


def send_reset_pass_email(user):
	subject = 'Reset your password'
	url = f'{SITE_URL}/reset/?u={user.uuid}'
	html = _render_template('reset_pass', {
		'headline': 'Hi,' + user.get_short_name(),
		'subject': subject,
		'url': url,
	})
	_send_email(subject, user.email, html)


def _render_template(template: str, context: dict = None) -> str:
	context['link_color'] = fake.color()  # '#d23049'
	context['phone_number'] = fake.phone_number()
	return str(get_template(f'postman/{template}.html').render(context))


def _send_email(subject: str, email: str, html: str) -> int:
	return send_mail(
		subject, strip_tags(html), None, [email], html_message=html)
