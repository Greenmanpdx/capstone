from django.contrib import admin

# Register your models here.
from .models import NPC, Character, Encounter, Monster, Session, PC

admin.site.register(NPC)

admin.site.register(Encounter)
admin.site.register(Monster)
admin.site.register(Session)
admin.site.register(PC)


