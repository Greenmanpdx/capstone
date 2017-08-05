
import csv
import pickle

class Circular_list(list):
    def __getitem__(self, item):
        try:
            return super(Circular_list, self).__getitem__(item)
        except IndexError:
            pass

        try:
            index = int(item)
            index = index % self.__len__()
            return super(Circular_list, self).__getitem__(index)
        except ValueError:
            raise TypeError


class Tracker:
    def __init__(self):
        self.turn_tracker = Circular_list()
        self.delayed_dict = {}

    def add_player(self, player):
        self.turn_tracker.append(player)

    def remove_player(self, index):
        del self.turn_tracker[index % len(self.turn_tracker)]

    def delay_turn(self, index):
        delayed = self.turn_tracker.pop(index % len(self.turn_tracker))
        i = str(len(self.delayed_dict) + 1)
        self.delayed_dict[i] = delayed

    def resume_turn(self, turn_index, delay_index):
        self.turn_tracker.insert(turn_index % len(self.turn_tracker), self.delayed_dict[delay_index])
        del self.delayed_dict[delay_index]

    def dump(self):
        data = pickle.dumps(self)
        return data





