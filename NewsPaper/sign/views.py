from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


@login_required
def upgrade_me(request):
    user = request.user
    authors = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors.user_set.add(user)
    return redirect('/')


@receiver(post_save, sender=User)
def send_registration_email(sender, instance, created, **kwargs):
    if created:
        subject = "Welcome to our site!"
        to = instance.email
        template_name = "email/registration_email.html"
        context = {
            "user": instance,
        }
        email_body = render_to_string(template_name, context)
        email = EmailMessage(
            subject=subject,
            body=email_body,
            from_email='какой то емейл',
            to=[to],
        )
        email.send()


class AddArticle(PermissionRequiredMixin, CreateView):
    permission_required = ('News.add_article',
                           'News.change_article')