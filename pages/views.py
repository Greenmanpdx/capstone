from django.shortcuts import render, HttpResponseRedirect
from .models import NPC, Encounter, Character, Monster, Session, PC
# from capstone.pages import search
from django.http import JsonResponse
from .serializers import NPCSerializer, CharacterSerializer, SessionSerializer, EncounterSerializer
from .search import get_query, normalize_query
import json
import re
import pickle


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
    delayed = Session.delay

    return render(request, 'pages/combat.html', {'session': session, 'delayed': delayed})


def initiative_tracker(request):
    if request.method == 'POST':
        session = Session.objects.get(pk=request.POST.get('pk'))
        session.first_pickle_list()
        session.save()
        tracker = pickle.loads(session.tracker)
        tracker.turn_tracker.sort()
        characters = tracker.turn_tracker
        session.delay = ''
        session.save()
        character_list = []
        delayed_list = []


        for c in characters:
            character_list.append({
                'name': c.name,
                'id': c.pk,
                'type': c.char_type

            })
        current_turn = character_list[0]

        return JsonResponse({'data': character_list, 'current': current_turn, 'delayed': delayed_list})


def next_turn(request):
    if request.method == 'POST':
        session = Session.objects.get(pk=request.POST.get('pk'))

        tracker = pickle.loads(session.tracker)

        tracker.turn_tracker.append(tracker.turn_tracker.pop(0))
        session.tracker = pickle.dumps(tracker)
        session.save()
        characters = tracker.turn_tracker
        character_list = []
        for c in characters:
            character_list.append({
                'name': c.name,
                'id': c.pk,
                'type': c.char_type

            })
        current_turn = character_list[0]
        print('tracker: {}'.format(tracker.turn_tracker))

        return JsonResponse({'data': character_list, 'current': current_turn})

def previous_turn(request):
    if request.method == 'POST':
        session = Session.objects.get(pk=request.POST.get('pk'))

        tracker = pickle.loads(session.tracker)


        tracker.turn_tracker.insert(0, tracker.turn_tracker.pop())
        session.tracker = pickle.dumps(tracker)
        session.save()
        characters = tracker.turn_tracker
        character_list = []
        for c in characters:
            character_list.append({
                'name': c.name,
                'id': c.pk,
                'type': c.char_type

            })
        current_turn = character_list[0]
        print('tracker: {}'.format(tracker.turn_tracker))

        return JsonResponse({'data': character_list, 'current': current_turn})


def delay_turn(request):
    if request.method == 'POST':
        session = Session.objects.get(pk=request.POST.get('pk'))
        tracker = pickle.loads(session.tracker)
        if session.delay:
            delayed = pickle.loads(session.delay)
        else:
            delayed = []

        delayed.append(tracker.turn_tracker.pop(0))

        session.tracker = pickle.dumps(tracker)
        session.delay = pickle.dumps(delayed)
        session.save()
        characters = tracker.turn_tracker
        character_list = []
        for c in characters:
            character_list.append({
                'name': c.name,
                'id': c.pk,
                'char_type': c.char_type

            })
        delayed_list = []
        for d in delayed:
            delayed_list.append({
                'name': d.name,
                'id': d.pk,
                'char_type': d.char_type
            })
        current_turn = character_list[0]
        print('tracker: {}'.format(tracker.turn_tracker))
        print('delayed: {}'.format(delayed))

        return JsonResponse({'data': character_list, 'delayed': delayed_list})


def resume_menu(request):
    if request.method == 'POST':
        session = Session.objects.get(pk=request.POST.get('pk'))
        tracker = pickle.loads(session.tracker)
        if session.delay:
            delayed = pickle.loads(session.delay)
        else:
            delayed = []

        # rCharacter = request.POST.get('toResume')
        # rType = request.POST.get('charType')

        charToPop = PC.objects.get(pk=request.POST.get('id'))
        if charToPop.char_type == 'pc':
            toPop = 'PC: ' + charToPop.name
        print(toPop)


        tracker.turn_tracker.insert(0, delayed.pop(delayed.index(charToPop)))
        print('tracker: {}'.format(tracker.turn_tracker))
        print('delayed: {}'.format(delayed))
        session.tracker = pickle.dumps(tracker)
        session.delay = pickle.dumps(delayed)
        session.save()
        characters = tracker.turn_tracker
        character_list = []
        for c in characters:
            character_list.append({
                'name': c.name,
                'id': c.pk,
                'type': c.char_type

            })
        delayed_list = []
        for d in delayed:
            delayed_list.append({
                'name': d.name,
                'id': d.pk,
                'type': d.char_type
            })

        return JsonResponse({'data': character_list, 'delayed': delayed_list})

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


        myDict = dict(request.POST)
        myList = myDict.items()
        for x in myList:

            y = x[0][12:-1]

            z = re.split('_', y)

            character_type = z[0]
            pk = z[1]
            initiative = str(x[1])[2:-2]
            if character_type == 'pc':
                character = PC.objects.get(pk=pk)
                character.initiative = initiative
                character.save()
            if character_type == 'npc':
                character = NPC.objects.get(pk=pk)
                character.initiative = initiative
                character.save()

        return JsonResponse({'message': "Hooray"})

def start_combat(request):
    session = Session.objects.get(pk=request.POST.get('pk'))
