from django.db import models
from . tracker import Tracker
from itertools import chain
from operator import attrgetter
from picklefield.fields import PickledObjectField
import pickle
# Create your models here.


class Character(models.Model):
    name = models.CharField(max_length=256)
    initiativeBonus = models.IntegerField(default=0)
    initiative = models.IntegerField(default=0)
    ac = models.IntegerField()
    char_type = models.CharField(max_length=10, default='npc')

    def __str__(self):
        return self.name

    def __lt__(self, other):
        if self.initiative == other.initiative:
            return self.initiativeBonus > other.initiativeBonus
        else:
            return self.initiative > other.initiative

    def __gt__(self, other):
        if self.initiative == other.initiative:
            return self.initiativeBonus < other.initiativeBonus
        else:
            return self.initiative < other.initiative

    def __eq__(self, other):
        if self.initiative == other.initiative:
            return self.initiativeBonus == other.initiativeBonus
        else:
            return self.initiative == other.initiative

    class Meta:
        abstract = True


class PC(Character):
    player_name = models.CharField(max_length=256, null=True, blank=True)


class NPC(Character):

    cr = models.FloatField()
    xp = models.IntegerField()
    race = models.CharField(max_length=256, null=True, blank=True)
    alignment = models.CharField(max_length=3)
    size = models.CharField(max_length=20)
    type = models.CharField(max_length=256)
    subtype1 = models.CharField(max_length=256, null=True, blank=True)
    subtype2 = models.CharField(max_length=256, null=True, blank=True)
    subtype3 = models.CharField(max_length=256, null=True, blank=True)
    subtype4 = models.CharField(max_length=256, null=True, blank=True)
    subtype5 = models.CharField(max_length=256, null=True, blank=True)
    subtype6 = models.CharField(max_length=256, null=True, blank=True)
    ac_touch = models.IntegerField()
    ac_ff = models.IntegerField()
    hp = models.IntegerField()
    hd = models.CharField(max_length=10)
    fort = models.CharField(max_length=20)
    ref = models.CharField(max_length=20)
    will = models.CharField(max_length=20)
    melee = models.CharField(max_length=256, null=True, blank=True)
    range = models.CharField(max_length=256, null=True, blank=True)
    space = models.CharField(max_length=5)
    reach = models.CharField(max_length=256, null=True, blank=True)
    str = models.CharField(max_length=3, null=True, blank=True)
    dex = models.CharField(max_length=3, null=True, blank=True)
    con = models.CharField(max_length=3, null=True, blank=True)
    int = models.CharField(max_length=3, null=True, blank=True)
    wis = models.CharField(max_length=3, null=True, blank=True)
    cha = models.CharField(max_length=3, null=True, blank=True)
    feats = models.CharField(max_length=256, null=True, blank=True)
    skills = models.CharField(max_length=1024, null=True, blank=True)
    languages = models.CharField(max_length=256, null=True, blank=True)
    special_quality = models.CharField(max_length=256, null=True, blank=True)
    environment = models.CharField(max_length=256)
    organization = models.CharField(max_length=256)
    treasure = models.CharField(max_length=256, null=True, blank=True)
    speed = models.CharField(max_length=256, null=True, blank=True)
    source = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return self.name + ' cr: ' + str(self.cr)


class Encounter(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return self.name


class Monster(models.Model):
    npc = models.ForeignKey('NPC')
    number = models.IntegerField(null=True)
    encounter = models.ForeignKey('Encounter', related_name='monsters')


class Session(models.Model):
    session_date = models.DateField()
    encounter = models.ForeignKey('Encounter', blank=True, null=True)
    pcs = models.ManyToManyField('PC', blank=True)
    tracker = PickledObjectField(null=True)
    delay = PickledObjectField(null=True)


    def __str__(self):
        return str(self.session_date)

    def extract_npcs(self, monsters):
        list = []
        for monster in monsters:
            for i in range(0, monster.number):
                list.append(monster.npc)
        return list

    def first_pickle_list(self):
        monster_list = [monster for monster in self.encounter.monsters.all()]
        npc_list = self.extract_npcs(monster_list)
        players_list = [p for p in self.pcs.all()]
        tracker = Tracker()
        result_list = sorted(
            chain(npc_list, players_list),
            key=attrgetter('initiative'),
            reverse=True)
        for x in result_list:
            tracker.add_player(x)
        self.tracker = pickle.dumps(tracker)


