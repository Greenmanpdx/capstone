import tracker





def check_delay(turn_list, index):
    print('Delaying: {}'.format(turn_list.delayed_dict))
    select = input('Does anyone want to take their turn?')
    if select == 'y' or select == 'Y':
        print_dict(turn_list.delayed_dict)
        undelayed = input('Select character')
        turn_list.resume_turn(index, undelayed)


def run_combat(turn_list):

    turn_list.turn_tracker.sort()
    combat_continue = True
    index = 0
    while combat_continue:
        if not turn_list.turn_tracker:
            global combat_continue
            combat_continue = False
            break
        if turn_list.delayed_dict:
            check_delay(turn_list, index)
        print(turn_list.turn_tracker[index])
        print(turn_list.turn_tracker)
        selection = input(
            '1. Next \n'
            '2. Previous \n'
            '3. delay \n'
            '4. kill \n'
            '5. quit')
        if selection == '1':
            index += 1
        elif selection == '2':
            index -= 1
        elif selection == '3':
            turn_list.delay_turn(index)
        elif selection == '4':
            turn_list.remove_player(index)
        elif selection == '5':
            combat_continue = False
