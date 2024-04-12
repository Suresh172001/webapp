from django.contrib import admin
from .models import *
# from django.contrib.auth.admin import UserAdmin
# Register your models here.

from django.contrib.auth import get_user_model
UserUsers = get_user_model()
admin.site.register(UserUsers)
