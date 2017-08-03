from django.contrib import admin

# Register your models here.
from .models import NPC, Character, Encouter, Monster, Session

admin.site.register(NPC)
admin.site.register(Character)
admin.site.register(Encouter)
admin.site.register(Monster)
admin.site.register(Session)

