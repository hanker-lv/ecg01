from django.contrib import admin
from .models import Person, EcgData
# Register your models here.
admin.site.register(Person)
admin.site.register(EcgData)
