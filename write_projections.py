"""
Create Optimal Lineup
"""

import sys
import getopt
import json
import pandas

QBS, RBS, WRS, TES, FLEX, DEFS = (pandas.DataFrame() for i in range(6))
SITE = ''
MAX_SALARY = {
    'DraftKings': 50000,
    'FanDuel': 60000,
}

def main(argv):
    """
    Write the Projected best lineup
    """

    global QBS, RBS, WRS, TES, FLEX, DEFS, SITE

    output_file_name, ending, key = '', '', ''

    try:
        opts, args = getopt.getopt(argv, "hs:e:o:k:", ["site="])
    except getopt.GetoptError:
        print('write-projections.py -s <Site | DraftKings or FanDuel>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('write-projections.py -s <Site | DraftKings or FanDuel>')
            sys.exit(1)
        elif opt == '-s':
            SITE = arg
        elif opt == '-e':
            ending = arg
        elif opt == '-o':
            output_file_name = arg
        elif opt == '-k':
            key = arg

    # Load dataset
    names = [
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

    sort = [key, 'salary']

    QBS = pandas.read_csv('./static/csv/' + SITE + '/nfl-qb' + ending + '.csv', names=names)\
        .sort_values(by=sort, ascending=False)\
        .reset_index()
    RBS = pandas.read_csv('./static/csv/' + SITE + '/nfl-rb' + ending + '.csv', names=names)\
        .sort_values(by=sort, ascending=False)\
        .reset_index()
    WRS = pandas.read_csv('./static/csv/' + SITE + '/nfl-wr' + ending + '.csv', names=names)\
        .sort_values(by=sort, ascending=False)\
        .reset_index()
    TES = pandas.read_csv('./static/csv/' + SITE + '/nfl-te' + ending + '.csv', names=names)\
        .sort_values(by=sort, ascending=False)\
        .reset_index()
    DEFS = pandas.read_csv('./static/csv/' + SITE + '/nfl-defense' + ending + '.csv', names=names)\
        .sort_values(by=sort, ascending=False)\
        .reset_index()

    QBS = add_point_per_dollar(QBS)
    RBS = add_point_per_dollar(RBS)
    WRS = add_point_per_dollar(WRS)
    TES = add_point_per_dollar(TES)
    DEFS = add_point_per_dollar(DEFS)

    FLEX = FLEX.append([RBS, WRS, TES])\
        .sort_values(by=sort, ascending=False)\
        .reset_index()

    lineups = {}
    lineup_indexes = reset()
    lineups['p_lineup'] = create_lineup(lineup_indexes, 'points_per_salary')
    lineup_indexes = reset()
    lineups['c_lineup'] = create_lineup(lineup_indexes, 'ceiling_per_salary')
    lineup_indexes = reset()
    lineups['f_lineup'] = create_lineup(lineup_indexes, 'floor_per_salary')
    # lineup_indexes = reset()
    # lineups['points_lineup'] = create_lineup(lineup_indexes, 'points')

    with open('./static/json/' + SITE + '/' + output_file_name + '.json', 'w') as file_printer:
        json.dump(lineups, file_printer)

def reset():
    """
    Reset the lineup indexes
    """
    lineup_indexes = {
        'QB': [0],
        'RB': [0, 1],
        'WR': [0, 1, 2],
        'TE': [0],
        'FLEX': [0],
        'DEFS': [0],
    }
    lineup_indexes['FLEX'][0] = get_flex_index(lineup_indexes)

    return lineup_indexes

def add_point_per_dollar(dataframe):
    """
    Add the points per salary values
    """
    dataframe['ceiling_per_salary'] = (dataframe['ceiling']*1000)/dataframe['salary']
    dataframe['floor_per_salary'] = (dataframe['floor']*1000)/dataframe['salary']
    dataframe['points_per_salary'] = (dataframe['points']*1000)/dataframe['salary']
    
    dataframe['ffa_ceiling_per_salary'] = (dataframe['ffa_ceiling']*1000)/dataframe['salary']
    dataframe['ffa_floor_per_salary'] = (dataframe['ffa_floor']*1000)/dataframe['salary']
    dataframe['ffa_points_per_salary'] = (dataframe['ffa_points']*1000)/dataframe['salary']

    return dataframe


def get_position(player_list, index):
    """
    Shortcut function to return the lineup position dict
    """
    return {
        'name': player_list['name'][index],
        'salary': player_list['salary'][index].item(),
        'points': player_list['points'][index],
        'ceiling': player_list['ceiling'][index],
        'floor': player_list['floor'][index],
        'ffa_points': player_list['ffa_points'][index],
        'ffa_ceiling': player_list['ffa_ceiling'][index],
        'ffa_floor': player_list['ffa_floor'][index],
        'points_per_salary': player_list['points_per_salary'][index].item(),
        'ceiling_per_salary': player_list['ceiling_per_salary'][index].item(),
        'floor_per_salary': player_list['floor_per_salary'][index].item(),
        'ffa_points_per_salary': player_list['ffa_points_per_salary'][index].item(),
        'ffa_ceiling_per_salary': player_list['ffa_ceiling_per_salary'][index].item(),
        'ffa_floor_per_salary': player_list['ffa_floor_per_salary'][index].item(),
    }


def get_least(player_list, indexes, comparator):
    """
    Return the difference between the least player and the next player in the list
    """
    least_valuable_index = indexes[0]
    for i in indexes:
        if player_list[comparator][i] < player_list[comparator][least_valuable_index]:
            least_valuable_index = i

    return {
        'value': player_list[comparator][least_valuable_index],
        'index': least_valuable_index,
    }


def get_new_lineup_indexes(lineup_indexes, comparator):
    """
    Return the indexes for the next lineup
    """
    flex_lineup = {
        'QB': lineup_indexes['QB'],
        'RB': lineup_indexes['RB'],
        'WR': lineup_indexes['WR'],
        'TE': lineup_indexes['TE'],
        'FLEX': [lineup_indexes['FLEX'][0]+1],
        'DEFS': lineup_indexes['DEFS'],
    }
    next_player_indexes = {
        'QB': lineup_indexes['QB'][len(lineup_indexes['QB'])-1]+1,
        'RB': lineup_indexes['RB'][len(lineup_indexes['RB'])-1]+1,
        'WR': lineup_indexes['WR'][len(lineup_indexes['WR'])-1]+1,
        'TE': lineup_indexes['TE'][len(lineup_indexes['TE'])-1]+1,
        'FLEX': get_flex_index(flex_lineup),
        'DEFS': lineup_indexes['DEFS'][len(lineup_indexes['DEFS'])-1]+1,
    }

    least_valuable_indexes = {
        'QB': get_least(QBS, lineup_indexes['QB'], comparator),
        'RB': get_least(RBS, lineup_indexes['RB'], comparator),
        'WR': get_least(WRS, lineup_indexes['WR'], comparator),
        'TE': get_least(TES, lineup_indexes['TE'], comparator),
        'FLEX': get_least(FLEX, lineup_indexes['FLEX'], comparator),
        'DEFS': get_least(DEFS, lineup_indexes['DEFS'], comparator),
    }

    max_index = {
        'QB': len(QBS['name']),
        'RB': len(RBS['name']),
        'WR': len(WRS['name']),
        'TE': len(TES['name']),
        'FLEX': len(FLEX['name']),
        'DEFS': len(DEFS['name']),
    }

    least_valuable_positions = get_least_valuable_positions(least_valuable_indexes)

    for value in least_valuable_positions:
        current_position = value['position']
        if next_player_indexes[current_position] < max_index[current_position]-1:
            lineup_indexes[current_position].remove(
                least_valuable_indexes[current_position]['index']
            )
            lineup_indexes[current_position].append(
                next_player_indexes[current_position]
            )
            break

    return lineup_indexes


def get_least_valuable_positions(least_valuable_indexes):
    """
    Return a sorted list of the least valuable positions
    """
    least_valuable_positions = [
        {
            'position': 'QB',
            'value': least_valuable_indexes['QB']['value'],
        },
        {
            'position': 'RB',
            'value': least_valuable_indexes['RB']['value'],
        },
        {
            'position': 'WR',
            'value': least_valuable_indexes['WR']['value'],
        },
        {
            'position': 'TE',
            'value': least_valuable_indexes['TE']['value'],
        },
        {
            'position': 'FLEX',
            'value': least_valuable_indexes['FLEX']['value'],
        },
        {
            'position': 'DEFS',
            'value': least_valuable_indexes['DEFS']['value'],
        },
    ]

    quicksort(least_valuable_positions, 0, len(least_valuable_positions)-1)

    return least_valuable_positions


def quicksort(arr, low, high):
    """
    Quick Sort algorithm
    """
    if low < high:
        pivot = partition(arr, low, high)

        quicksort(arr, low, pivot-1)
        quicksort(arr, pivot+1, high)


def partition(arr, low, high):
    """
    Partition for Quick Sort
    """
    pivot = arr[high]['value']
    i = (low - 1)

    for j in range(low, high):
        if arr[j]['value'] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i+1], arr[high] = arr[high], arr[i+1]
    return i+1


def get_flex_index(lineup_indexes):
    """
    Return the flex index
    """
    for i in lineup_indexes['RB']:
        if FLEX['name'][lineup_indexes['FLEX'][0]] == RBS['name'][i]:
            lineup_indexes['FLEX'][0] += 1
            return get_flex_index(lineup_indexes)

    for i in lineup_indexes['WR']:
        if FLEX['name'][lineup_indexes['FLEX'][0]] == WRS['name'][i]:
            lineup_indexes['FLEX'][0] += 1
            return get_flex_index(lineup_indexes)

    for i in lineup_indexes['TE']:
        if FLEX['name'][lineup_indexes['FLEX'][0]] == TES['name'][i]:
            lineup_indexes['FLEX'][0] += 1
            return get_flex_index(lineup_indexes)

    return lineup_indexes['FLEX'][0]


def create_lineup(lineup_indexes, comparator):
    """
    Create a valid lineup
    """
    lineup = {
        'players': {
            'qb': get_position(QBS, lineup_indexes['QB'][0]),
            'rb1': get_position(RBS, lineup_indexes['RB'][0]),
            'rb2': get_position(RBS, lineup_indexes['RB'][1]),
            'wr1': get_position(WRS, lineup_indexes['WR'][0]),
            'wr2': get_position(WRS, lineup_indexes['WR'][1]),
            'wr3': get_position(WRS, lineup_indexes['WR'][2]),
            'te': get_position(TES, lineup_indexes['TE'][0]),
            'flex': get_position(FLEX, lineup_indexes['FLEX'][0]),
            'defs': get_position(DEFS, lineup_indexes['DEFS'][0]),
        }
    }

    cost = 0
    total_points = 0
    total_ceiling = 0
    total_floor = 0
    ffa_total_points = 0
    ffa_total_ceiling = 0
    ffa_total_floor = 0

    for key, player in lineup['players'].items():
        cost += player['salary']
        total_points += player['points']
        total_ceiling += player['ceiling']
        total_floor += player['floor']
        ffa_total_points += player['ffa_points']
        ffa_total_ceiling += player['ffa_ceiling']
        ffa_total_floor += player['ffa_floor']

    lineup['cost'] = cost
    lineup['total_points'] = total_points
    lineup['ceiling'] = total_ceiling
    lineup['floor'] = total_floor
    lineup['ffa_total_points'] = ffa_total_points
    lineup['ffa_ceiling'] = ffa_total_ceiling
    lineup['ffa_floor'] = ffa_total_floor

    if lineup['cost'] > MAX_SALARY[SITE]:
        lineup_indexes = get_new_lineup_indexes(lineup_indexes, comparator)
        return create_lineup(lineup_indexes, comparator)

    return lineup


if __name__ == "__main__":
    main(sys.argv[1:])
