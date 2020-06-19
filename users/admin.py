from django.contrib import admin
from .models import Users,Cohort,Profile
from django.contrib.auth.admin import UserAdmin


admin.site.register(Users)
admin.site.register(Cohort)
admin.site.register(Profile)

