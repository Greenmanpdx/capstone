from django.shortcuts import render, HttpResponseRedirect
from .models import NPC, Encouter, Character, Monster, Session
# from capstone.pages import search
from django.http import JsonResponse
from .serializers import NPCSerializer, CharacterSerializer, SessionSerializer, EncounterSerializer, InitiativeSerializer
from .search import get_query, normalize_query


def home(request):
    enc = Encouter.objects.all()
    character = Character.objects.all()
    session = Session.objects.all()

    return render(request, 'pages/home.html', {'enc': enc, 'character': character, 'session': session})


def encounter_builder(request, pk):
    enc = Encouter.objects.get(pk=pk)

    return render(request, 'pages/encounterBuilder.html', {'enc': enc})


def search_api(request):
    if request.method == 'POST':
        print(request.POST)
    npcs = NPC.objects.filter(
        name__contains=request.POST.get('name')).filter(
        cr__gte=request.POST.get('crLow')).filter(
        cr__lte=request.POST.get('crHigh')).filter(
        environment__contains=request.POST.get('environment')).filter(
        type__contains=request.POST.get('type'))


    s = NPCSerializer(npcs, many=True)
    return JsonResponse({'data': s.data})


def create_encounter(request):
    if request.method == 'POST':
        print(request.POST)
        enc = Encouter()
        enc.name = request.POST.get('encounterName')
        enc.description = request.POST.get('description')
        enc.save()
        return HttpResponseRedirect("/encounters/{}/".format(enc.pk))


def create_player(request):
    if request.method == 'POST':
        print(request.POST)
        char = Character()
        char.name = request.POST.get('chracterName')
        char.initiativeBonus = request.POST.get('initiativeBonus')
        char.ac = request.POST.get('ac')
        char.save()
        return HttpResponseRedirect("/")


def add_monster_api(request):
    if request.method == 'POST':
        print(request.POST)
        npc = NPC.objects.get(pk=request.POST.get('pk'))
        encounter = Encouter.objects.get(pk=request.POST.get('enc'))
        Monster.objects.create(npc=npc, number=int(request.POST.get('numb')), encounter=encounter)
        return JsonResponse({'message': 'success'})
    return JsonResponse({'message': 'failure, you suck'})

def player_to_session(request):
    if request.method == 'POST':
        character = Character.objects.get(pk=request.POST.get('pk'))
        session = Session.objects.get(pk=request.POST.get('sessionId'))
        session.players.add(character)
        session.save()
        p = CharacterSerializer(character)
        return JsonResponse({'data': p.data})


def create_session(request):
    if request.method == 'POST':
        from dateutil import parser
        session_date = parser.parse(request.POST.get('date'))

        session = Session.objects.create(session_date=session_date)
        return JsonResponse({'message': 'success', 'id': session.id})
    return JsonResponse({'message': 'failure, you suck'})

def encounter_to_session(request):
    if request.method == 'POST':
        print(request.POST)
        encounter = Encouter.objects.get(pk=request.POST.get('pk'))
        session = Session.objects.get(pk=request.POST.get('sessionId'))
        session.encounter.add(encounter)
        e = EncounterSerializer(encounter)
        return JsonResponse({'data': e.data})

def set_session(request):
    if request.method == 'POST':
        session = Session.objects.get(pk=request.POST.get('pk'))
        s = SessionSerializer(session)
        return JsonResponse({'data': s.data})



def combat(request, pk):
    session = Session.objects.get(pk=pk)

    return render(request, 'pages/combat.html', {'session': session})

def initiative_tracker(request):
    if request.method == 'POST':
        session = Session.objects.get(pk=request.POST.get('pk'))
        i = InitiativeSerializer(session)
        return JsonResponse({'data': i.data})
