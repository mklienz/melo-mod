from typing import List
from itertools import permutations
from collections import defaultdict


class ELOPlayer:
    def __init__(self, name: str, place: int, elo: float):
        self.name = name
        self.place = place
        self.elo = elo


class ELOMatch:
    def __init__(self, players: List[ELOPlayer] = []):
        self.players = players

    def add_elo_player(self, player: ELOPlayer):
        self.players.append(player)

    def calc_new_elos(self):
        n = len(self.players)
        K = 32
        avg_rating = sum([player.elo for player in self.players])/n
        elo_changes = defaultdict(float)
        for i in range(n):
            E = 1.0 / (1.0 + 10.0 ** ((avg_rating - self.players[i].elo) / 400)) * (2 / n)
            S = float(self.players[i].place == 10) # Works for Catan only
            elo_changes[i] += K * (S - E)

        for i in range(n):
            self.players[i].elo += round(elo_changes[i], 2)

    def get_player_names(self):
        return [player.name for player in self.players]

    def get_player_elo(self, player_name: str):
        for player in self.players:
            if player.name == player_name:
                return player.elo
