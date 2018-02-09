from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    pass
admin.site.register(User, UserAdmin)


class TellerAdmin(admin.ModelAdmin):
    pass
admin.site.register(Teller, TellerAdmin)


class CountryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Country, CountryAdmin)


class ServiceAdmin(admin.ModelAdmin):
    pass
admin.site.register(Service, ServiceAdmin)
