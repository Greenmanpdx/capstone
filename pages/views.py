from django.shortcuts import render, HttpResponseRedirect
from .models import NPC, Encounter, Character, Monster, Session, PC
# from capstone.pages import search
from django.http import JsonResponse
from .serializers import NPCSerializer, CharacterSerializer, SessionSerializer, EncounterSerializer
from .search import get_query, normalize_query
import json


def home(request):
    enc = Encounter.objects.all()
    pc = PC.objects.all()

    session = Session.objects.all()

    return render(request, 'pages/home.html', {'enc': enc, 'pc': pc, 'session': session})


def encounter_builder(request, pk):
    enc = Encounter.objects.get(pk=pk)

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
        enc = Encounter()
        enc.name = request.POST.get('encounterName')
        enc.description = request.POST.get('description')
        enc.save()
        return HttpResponseRedirect("/encounters/{}/".format(enc.pk))


def create_player(request):
    if request.method == 'POST':
        print(request.POST)
        pc = PC()
        pc.name = request.POST.get('chracterName')
        pc.initiativeBonus = request.POST.get('initiativeBonus')
        pc.ac = request.POST.get('ac')
        pc.char_type = 'pc'
        pc.save()
        return HttpResponseRedirect("/")


def add_monster_api(request):
    if request.method == 'POST':
        print(request.POST)
        npc = NPC.objects.get(pk=request.POST.get('pk'))
        encounter = Encounter.objects.get(pk=request.POST.get('enc'))
        Monster.objects.create(npc=npc, number=int(request.POST.get('numb')), encounter=encounter)
        return JsonResponse({'message': 'success'})
    return JsonResponse({'message': 'failure, you suck'})


def player_to_session(request):
    if request.method == 'POST':
        pc = PC.objects.get(pk=request.POST.get('pk'))
        session = Session.objects.get(pk=request.POST.get('sessionId'))
        session.pcs.add(pc)
        session.save()
        p = CharacterSerializer(pc)
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
        encounter = Encounter.objects.get(pk=request.POST.get('pk'))
        session = Session.objects.get(pk=request.POST.get('sessionId'))
        session.encounter = encounter
        session.save()
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
        session.first_pickle_list()
        session.save()

        return JsonResponse({'data': i.data})


def set_initiatve_window(request):
    if request.method == 'POST':
        session = Session.objects.get(pk=request.POST.get('pk'))
        npcList = []
        for p in session.pcs.all():
            npcList.append({
                'name': p.name,
                'id': p.pk,
                'type': p.char_type
            })
        for n in session.encounter.monsters.all():
            npcList.append({
                'name': n.npc.name,
                'number': n.number,
                'id': n.npc.pk,
                'type': n.npc.char_type
            })

        return JsonResponse({'data': npcList})


def set_initiative(request):
    if request.method == 'POST':
        session = Session.objects.get(pk=request.POST.get('pk'))
        print(request.POST)
        for x in request.POST.getlist('initiatives[]'):
            print(json.dumps(x))
        return JsonResponse({'message': "Hooray"})

def start_combat(request):
    pass