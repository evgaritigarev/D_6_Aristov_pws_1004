from django.db import models
from django.contrib.auth.models import User
from News.utils import send_email


class Article(models.Model):
    name = models.CharField(max_length=128)
    dateCreation = models.DateTimeField(auto_now_add=True)
    post = models.TextField()

    def __str__(self):
        return f'{self.name.title()}'
    
    def get_absolute_url(self):
        return f'/article/{self.id}'
    
    def send_notification_email(self):
        subject = f'New Article: {self.name}'
        message = f'Check out my new article "{self.name}" at {self.get_absolute_url()}'
        send_email(User.email, subject, message)
