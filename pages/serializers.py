from .models import NPC, Character, Encouter, Session, Monster
from rest_framework import serializers


class NPCSerializer(serializers.ModelSerializer):
    class Meta:
        model = NPC
        fields = '__all__'


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = '__all__'




class EncounterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Encouter
        fields = '__all__'


class SessionSerializer(serializers.ModelSerializer):
    encounter = EncounterSerializer(many=True)
    players = CharacterSerializer(many=True)
    class Meta:
        model = Session
        fields = ('id', 'session_date', 'encounter', 'players')

class MonsterSerializer(serializers.ModelSerializer):
    encounter = EncounterSerializer(source='encounter_set')
     class Meta:
        model = Monster
        fields = '__all__'

class InitiativeSerializer(serializers.ModelSerializer):
    players = CharacterSerializer(many=True)
    npcs = NPCSerializer(many=True)
    monster = MonsterSerializer(many=True)
    class Meta:
        model = Session
        fields = ('id', 'session_date', 'players', 'npcs')