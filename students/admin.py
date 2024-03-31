# your_app/admin.py
from django.contrib import admin
from .models import *


admin.site.register(GeneralBook)
admin.site.register(Journal)
admin.site.register(Paper)
admin.site.register(Novel)
