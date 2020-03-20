from django.contrib import admin
from .models import Institution, InstitutionNetwork, InstitutionEmail

admin.site.register(Institution)
admin.site.register(InstitutionNetwork)
admin.site.register(InstitutionEmail)
