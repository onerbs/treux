from django.core.mail import send_mail
from django.utils.html import strip_tags

from treux import future


@future.task(name='Send one email.')
def send_email(subject: str, email: str, html: str):
	send_mail(subject, strip_tags(html), None, [email], html_message=html)
