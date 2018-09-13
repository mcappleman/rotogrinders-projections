"""
Create Optimal Lineup
"""

import sys
import getopt
import pandas
import json

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

    output_file_name = ''

    try:
        opts, args = getopt.getopt(argv, "hs:o:", ["site="])
    except getopt.GetoptError:
        print('write-projections.py -s <Site | DraftKings or FanDuel>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('write-projections.py -s <Site | DraftKings or FanDuel>')
            sys.exit(1)
        elif opt == '-s':
            SITE = arg
        elif opt == '-o':
            output_file_name = arg

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
        'ceiling_per_salary',
        'floor_per_salary',
        'points_per_salary',
    ]

    qb_url = './static/csv/' + SITE + '/nfl-qb.csv'
    rb_url = './static/csv/' + SITE + '/nfl-rb.csv'
    wr_url = './static/csv/' + SITE + '/nfl-wr.csv'
    te_url = './static/csv/' + SITE + '/nfl-te.csv'
    d_url = './static/csv/' + SITE + '/nfl-defense.csv'
    sort = ['points', 'salary']

    QBS = pandas.read_csv(qb_url, names=names)\
        .sort_values(by=sort, ascending=False)\
        .reset_index()
    RBS = pandas.read_csv(rb_url, names=names)\
        .sort_values(by=sort, ascending=False)\
        .reset_index()
    WRS = pandas.read_csv(wr_url, names=names)\
        .sort_values(by=sort, ascending=False)\
        .reset_index()
    TES = pandas.read_csv(te_url, names=names)\
        .sort_values(by=sort, ascending=False)\
        .reset_index()
    DEFS = pandas.read_csv(d_url, names=names)\
        .sort_values(by=sort, ascending=False)\
        .reset_index()

    QBS = add_point_per_dollar(QBS)
    RBS = add_point_per_dollar(RBS)
    WRS = add_point_per_dollar(WRS)
    TES = add_point_per_dollar(TES)
    DEFS = add_point_per_dollar(DEFS)

    FLEX = FLEX.append([RBS, WRS, TES])\
        .sort_values(by=['points', 'salary'], ascending=False)\
        .reset_index()

    lineups = {}
    lineup_indexes = reset()
    lineups['p_lineup'] = create_lineup(lineup_indexes, 'points_per_salary')
    lineup_indexes = reset()
    lineups['c_lineup'] = create_lineup(lineup_indexes, 'ceiling_per_salary')
    lineup_indexes = reset()
    lineups['f_lineup'] = create_lineup(lineup_indexes, 'floor_per_salary')

    with open('./static/json/' + SITE + '/' + output_file_name + '.json', 'w') as fp:
        json.dump(lineups, fp)

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
        'points_per_salary': player_list['points_per_salary'][index].item(),
        'ceiling_per_salary': player_list['ceiling_per_salary'][index].item(),
        'floor_per_salary': player_list['floor_per_salary'][index].item(),
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

    least_valuable_position = 'QB'
    for key, value in least_valuable_indexes.items():
        if value['value'] < least_valuable_indexes[least_valuable_position]['value']:
            if SITE != 'FanDuel' or key != 'TE': 
                least_valuable_position = key

            if SITE == 'FanDuel' and key == 'TE' and (value['value']+.2) < least_valuable_indexes[least_valuable_position]['value']:
                least_valuable_position = key

    lineup_indexes[least_valuable_position].remove(\
        least_valuable_indexes[least_valuable_position]['index']\
        )
    lineup_indexes[least_valuable_position].append(next_player_indexes[least_valuable_position])

    return lineup_indexes


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
    # print(lineup_indexes)
    # print(TES['name'][lineup_indexes['TE'][0]] + ', ' + str(TES['points'][lineup_indexes['TE'][0]]) + ', ' + str(TES['points_per_salary'][lineup_indexes['TE'][0]]))
    # print()
    lineup = {
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

    cost = 0
    total_points = 0
    total_ceiling = 0
    total_floor = 0

    for key, player in lineup.items():
        cost += player['salary']
        total_points += player['points']
        total_ceiling += player['ceiling']
        total_floor += player['floor']

    lineup['cost'] = cost
    lineup['total_points'] = total_points
    lineup['ceiling'] = total_ceiling
    lineup['floor'] = total_floor

    if lineup['cost'] > MAX_SALARY[SITE]:
        lineup_indexes = get_new_lineup_indexes(lineup_indexes, comparator)
        return create_lineup(lineup_indexes, comparator)

    return lineup


if __name__ == "__main__":
    main(sys.argv[1:])
