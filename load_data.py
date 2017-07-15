import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'capstone.settings')

import django

django.setup()
import csv

from encounters.models import NPC

with open('beastiary.csv', newline='') as csvfile:
    r = csv.DictReader(csvfile)
    for i in r:
        npc = NPC()
        npc.name = i['Name']
        npc.cr = float(i['CR'])
        npc.xp = int(''.join(i['XP'].split(',')))
        npc.race = i['Race']
        npc.alignment = i['Alignment']
        npc.size = i['Size']
        npc.type = i['Type']
        npc.subtype1 = i['subtype1']
        npc.subtype2 = i['subtype2']
        npc.subtype3 = i['subtype3']
        npc.subtype4 = i['subtype4']
        npc.subtype5 = i['subtype5']
        npc.subtype6 = i['subtype6']
        npc.ac = int(i['AC'])
        npc.ac_touch = int(i['AC_Touch'])
        npc.ac_ff = 0 if i['AC_Flat-footed'] == '' else int(i['AC_Flat-footed'])
        npc.hp = int(i['HP'])
        npc.hd = i['HD']
        npc.fort = i['Fort']
        npc.ref = i['Ref']
        npc.will = i['Will']
        npc.melee = i['Melee']
        npc.range = i['Ranged']
        npc.space = i['Space']
        npc.reach = i['Reach']
        npc.str = 0 if i['Str'] == '-' else int(i['Str'])
        npc.dex = 0 if i['Dex'] == '-' else int(i['Dex'])
        npc.dex = 0 if i['Con'] == '-' else int(i['Con'])
        npc.int = 0 if i['Int'] == '-' else int(i['Int'])
        npc.wis = 0 if i['Wis'] == '-' else int(i['Wis'])
        npc.cha = 0 if i['Cha'] == '-' else int(i['Cha'])
        npc.feats = i['Feats']
        npc.skills = i['Skills']
        npc.languages = i['Languages']
        npc.special_quality = i['SQ']
        npc.environment = i['Environment']
        npc.organization = i['Organization']
        npc.treasure = i['Treasure']
        npc.speed = i['Speed']
        npc.source = i['Source']
        npc.save()
