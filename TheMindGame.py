import numpy as np
import torch
import random


class Player:

    def __init__(self, name, level):
        self.name = name
        self.level = level
        self.cards = []
        self.timer = np.inf
        self.aggresiveness = np.random.random_integers(low=1, high=3)

    def __str__(self):
        return "Name: " + str(self.name) + '\n' + "Cards: " + str(self.cards)

    def get_name(self):
        return self.name

    def set_level(self, level):
        self.level = level

    def draw_cards(self, deck):
        self.cards = deck.get_all_cards()[-self.level:]
        deck.set_cards(deck.get_all_cards()[:-self.level])

    def remove_card(self, card):
        if card not in self.cards:
            print("You don't have card ", str(card))
            print("Please choose another card")
        self.cards.remove(card)

    def play_card(self, table):
        if not self.is_empty_hand():
            # if card not in self.cards:
            #     print("You don't have card ", str(card))
            #     print("Please choose another card")
            # else:
            smallest_card = min(self.cards)
            self.remove_card(smallest_card)
            table.add_card(smallest_card)
            return smallest_card
        else:
            print(self.name, " has empty hand and cannot play the card.")

    def is_empty_hand(self):
        return len(self.cards) == 0

    def dec_timer(self):
        self.timer = self.timer - 1

    def read_timer(self):
        return self.timer

    def update_timer(self, table):
        # TODO
        self.timer = np.random.random_integers(
            low=1, high=5) * self.aggresiveness


class Table:

    def __init__(self):
        self.cards = []

    def __str__(self):
        return str(self.show_all_cards())

    def add_card(self, card):
        self.cards.append(card)

    def show_all_cards(self):
        return self.cards

    def show_top_card(self):
        return self.cards[-1]


class Deck:

    def __init__(self, total_num_cards):
        all_cards = np.arange(total_num_cards) + 1
        np.random.shuffle(all_cards)
        self.deck = all_cards.tolist()

    def __str__(self):
        pass

    def get_all_cards(self):
        return self.deck

    def set_cards(self, new_cards):
        self.deck = new_cards


class Clock:

    def __init__(self):
        self.time = 0

    def __str__(self):
        return "Current time step is " + str(self.time)

    def read_time(self):
        return self.time

    def step(self):
        self.time = self.time + 1

    def reset(self):
        self.time = 0


class Game:

    def __init__(self, player_names, level, total_num_cards, verbose=False):
        self.player_names = player_names
        self.players_list = [Player(name, level) for name in player_names]
        self.retired_players = []
        self.players = {
            player.get_name(): player for player in self.players_list}
        self.table = Table()
        self.deck = Deck(total_num_cards)
        self.clock = Clock()
        self.game_ended = False
        self.verbose = verbose

    def step(self):
        self.clock.step()
        if self.verbose:
            print("\n ---------------- t =",
                  self.clock.read_time(), " ----------------")
        for player in self.players:
            if not self.players[player].is_empty_hand():
                self.players[player].dec_timer()
                # print(self.players[player].read_timer())

        any_play = [i for i in range(len(self.players_list)) if self.players_list[i].read_timer(
        ) == 0 and not self.players_list[i].is_empty_hand()]
        # print(any_play)
        if not len(any_play) == 0:
            chosen_player = random.choice(any_play)
            print("* Chosen player: ",
                  self.players_list[chosen_player].get_name(), "\n")
            played_card = self.players_list[chosen_player].play_card(
                self.table)
            # print(self.players_list[chosen_player].name, " played ", str(played_card))
            for player in self.players_list:
                player.update_timer(self.table)

        not_all_empty = False
        for player in self.players_list:
            not_all_empty = not_all_empty or not player.is_empty_hand()
        self.game_ended = not not_all_empty

        # display states for each player
        if self.verbose == True:
            for ind in self.players:
                current_player = self.players[ind]
                print(current_player.get_name(), ": timer=",
                      current_player.read_timer(), "; hands=", current_player.cards)
            print("On the table: ", self.table.show_all_cards())
    def play(self):
        for player in self.players_list:
            player.draw_cards(self.deck)
            player.update_timer(self.table)

        while (self.game_ended == False):
        # for p in range(10):
            self.step()

if __name__ == "__main__":

    players = ["Ellen", "James", "Peilun"]
    g = Game(players, level=3, total_num_cards=10, verbose=True)
    g.play()
