from django.contrib import admin

from .models import Country, EmailConfirmationCode, Profile, User

admin.site.register(User)
admin.site.register(Country)
admin.site.register(EmailConfirmationCode)
admin.site.register(Profile)
