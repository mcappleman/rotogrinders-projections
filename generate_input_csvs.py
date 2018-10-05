"""
Generate the various input csvs for 1 and 1&4 games
"""

import sys
import getopt
import pandas

GAMES = {
    'ARI': 4,
    'ATL': 1,
    'BAL': 1,
    'BUF': 1,
    'CAR': 1,
    'CHI': 0,
    'CIN': 1,
    'CLE': 1,
    'DAL': 8,
    'DEN': 1,
    'DET': 1,
    'GBP': 1,
    'HOU': 8,
    'IND': 7,
    'JAC': 1,
    'KCC': 1,
    'LAC': 4,
    'LAR': 4,
    'MIA': 1,
    'MIN': 4,
    'NEP': 7,
    'NOS': 9,
    'NYG': 1,
    'NYJ': 1,
    'OAK': 4,
    'PHI': 4,
    'PIT': 1,
    'SEA': 4,
    'SFO': 4,
    'TBB': 0,
    'TEN': 1,
    'WAS': 9,
}

NAMES = [
    'name',
    'salary',
    'team',
    'position',
    'opponent',
    'ceiling',
    'floor',
    'points',
    'ffa_ceiling',
    'ffa_floor',
    'ffa_points',
    'ceiling_per_salary',
    'floor_per_salary',
    'points_per_salary',
    'ffa_ceiling_per_salary',
    'ffa_floor_per_salary',
    'ffa_points_per_salary',
]

def main():
    """
    Main function
    """
    draft_kings = 'DraftKings'
    fanduel = 'FanDuel'
    generate_csvs(draft_kings, 'qb')
    generate_csvs(fanduel, 'qb')

    generate_csvs(draft_kings, 'rb')
    generate_csvs(fanduel, 'rb')

    generate_csvs(draft_kings, 'wr')
    generate_csvs(fanduel, 'wr')

    generate_csvs(draft_kings, 'te')
    generate_csvs(fanduel, 'te')
    
    generate_csvs(draft_kings, 'defense')
    generate_csvs(fanduel, 'defense')


def generate_csvs(site, position):
    """
    Take in a site and position and write both the csvs for that site and position
    """
    all_players = pandas.read_csv('./static/csv/' + site + '/nfl-' + position + '.csv', header=None, names=NAMES)\
        .sort_values(by=['points', 'salary'], ascending=False)\
        .reset_index()

    players_1 = []
    players_1_4 = []

    for index, row in all_players.iterrows():
        player = {
            'name': row['name'],
            'salary': row['salary'],
            'team': row['team'],
            'position': row['position'],
            'opponent': row['opponent'],
            'ceiling': row['ceiling'],
            'floor': row['floor'],
            'points': row['points'],
            'ffa_ceiling': row['ffa_ceiling'],
            'ffa_floor': row['ffa_floor'],
            'ffa_points': row['ffa_points'],
        }
        if GAMES[player['team']] == 1:
            players_1.append(player)
            players_1_4.append(player)
        elif GAMES[player['team']] == 4:
            players_1_4.append(player)
        
    columns_order = ['name', 'salary', 'team', 'position', 'opponent', 'ceiling', 'floor', 'points', 'ffa_ceiling', 'ffa_floor', 'ffa_points']
    pandas.DataFrame(players_1).to_csv('./static/csv/' + site + '/nfl-' + position + '_1.csv', index=False, header=False, columns=columns_order)
    pandas.DataFrame(players_1_4).to_csv('./static/csv/' + site + '/nfl-' + position + '_1&4.csv', index=False, header=False, columns=columns_order)


if __name__ == '__main__':
    main()
    
