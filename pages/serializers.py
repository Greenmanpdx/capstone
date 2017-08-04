from .models import NPC, Character, Encounter, Session, Monster, PC
from rest_framework import serializers


class NPCSerializer(serializers.ModelSerializer):
    class Meta:
        model = NPC
        fields = '__all__'


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = PC
        fields = '__all__'


class MonsterSerializer(serializers.ModelSerializer):
    npc = NPCSerializer(many=True)
    class Meta:
        model = Monster
        fields = ('NPC', 'number')


class EncounterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Encounter
        fields = '__all__'


class SessionSerializer(serializers.ModelSerializer):
    encounter = EncounterSerializer()
    pcs = CharacterSerializer(many=True)

    class Meta:
        model = Session
        fields = ('id', 'session_date', 'encounter', 'pcs')




