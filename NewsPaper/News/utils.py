from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
# from .models import Article


def send_email(self):
    subject = "New Article"
    to = self.user.email
    template_name = "email/create_article.html"
    context = {
        "object": self,
    }
    email_body = render_to_string(template_name, context)
    email = EmailMessage(
        subject=subject,
        body=email_body,
        from_email='какой то емейл',
        to=[to],
    )
    email.send()

def save(self, *args, **kwargs):
    is_new = not self.pk
    super(Article, self).save(*args, **kwargs)
    if is_new:
        self.send_email()