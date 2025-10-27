from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created
from django.utils.html import strip_tags
from django.conf import settings
# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is a requare')
        

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=200, unique=True)
    bithday = models.DateField(null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)

    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []





# reset password
@receiver(reset_password_token_created)
def reset_password_token_created(reset_password_token, *args, **kwargs):
    sitelink = "http://localhost:5173/"
    token = "?token={}".format(reset_password_token.key)
    full_link = str(sitelink)+str('password-reset')+str(token)

    print(token)
    print(full_link)

    context = {
        'full_link': full_link,
        'email_address': reset_password_token.user.email
    }

    html_massage= render_to_string("backend/resetpass.html", context=context)
    plain_massage = strip_tags(html_massage)

    msg = EmailMultiAlternatives(
        subject = "request for reset password".format(title=reset_password_token.user.email),
        body=plain_massage,
        from_email=f"My App <{settings.EMAIL_HOST_USER}>",
        to = [reset_password_token.user.email]
    )

    msg.attach_alternative(html_massage, "text/html") 
    try:
        msg.send()
        print("✅ Email sent successfully!")
    except Exception as e:
        print("❌ Email sending failed:", e)
