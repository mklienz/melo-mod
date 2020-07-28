import csv
import sys
from elo import ELOPlayer, ELOMatch

STARTING_ELO = 1200

# Open file
with open(sys.argv[1]) as input_file:
    csv_reader = csv.DictReader(input_file)

    for line_count, row in enumerate(csv_reader):
        if line_count == 0:
            # On first row, set up ELO table as a dictionary
            # Date + Names as keys
            # keep a copy of player names
            player_elos = {k: [] for k in row.keys()}
            player_names = list(player_elos.keys())[1:]
            DATE_COL_NAME = list(player_elos.keys())[0]
            player_elos[DATE_COL_NAME].append(row[DATE_COL_NAME])
            for name in player_names:
                player_elos[name].append(STARTING_ELO)

        # Create each player as required for match - input is a list of ELOPlayers
        match = ELOMatch([])
        for name, score in list(row.items())[1:]:
            score = int(score)
            if score > 0:
                match.add_elo_player(ELOPlayer(name, score, player_elos[name][-1]))
        # Use the calcuate new elos function to calculate new elos for teh given players
        match.calc_new_elos()

        # Update ELOS dict
        match_players = match.get_player_names()
        player_elos[DATE_COL_NAME].append(row[DATE_COL_NAME])
        for name in player_names:
            if name in match_players:
                player_elos[name].append(match.get_player_elo(name))
            else:
                player_elos[name].append(player_elos[name][-1])
        print(player_elos)
