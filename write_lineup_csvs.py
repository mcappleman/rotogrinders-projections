"""
Write a CSV for comparing all the lineups for a given week
"""

import sys
import getopt
import json
import pandas

LINEUPS = {
    'DraftKings' : {},
    'FanDuel': {},
}

SITES = ['DraftKings', 'FanDuel']

def main(argv):
    """
    Main
    """

    week = 0

    try:
        opts, args = getopt.getopt(argv, "hw:", ["week="])
    except getopt.GetoptError:
        print('python write_lineup_csvs.py -w <Week>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('python write_lineup_csvs.py -w <Week>')
            sys.exit(1)
        elif opt == '-w':
            week = arg

    path = './static/json'
    populate_LINEUPS(path, week)
    csv_path = './static/csv'
    write_csvs(csv_path)


def populate_LINEUPS(path, week):
    """
    Populate LINEUPS global var
    """
    for site in SITES:
        populate_JSON(path, site, 'PointsSort', week)
        populate_JSON(path, site, 'CeilingSort', week)
        populate_JSON(path, site, 'FloorSort', week)

        populate_JSON(path, site, 'FFA_PointsSort', week)
        populate_JSON(path, site, 'FFA_CeilingSort', week)
        populate_JSON(path, site, 'FFA_FloorSort', week)


def populate_JSON(file_path, site, file_name, week):
    """
    Get JSON lineup files for the given week
    """
    file_path = file_path + '/' + site + '/' + file_name + 'Week' + week + '.json'
    with open(file_path) as f:
        LINEUPS[site][file_name] = json.load(f)


def write_csvs(csv_base):
    """
    Create Dataframe and write csv
    """
    for site in SITES:
        local_path = csv_base + '/' + site + '/lineup_comparison.csv'
        site_lineups = {
            'name': [],
            'roto_points': [],
            'roto_ceiling': [],
            'roto_floor': [],
            'ffa_points': [],
            'ffa_ceiling': [],
            'ffa_floor': [],
        }

        for key, value in LINEUPS[site].items():
            index = 1
            for k, v in value.items():
                site_lineups['name'].append(key + str(index))
                site_lineups['roto_points'].append(v['total_points'])
                site_lineups['roto_ceiling'].append(v['ceiling'])
                site_lineups['roto_floor'].append(v['floor'])
                site_lineups['ffa_points'].append(v['ffa_total_points'])
                site_lineups['ffa_ceiling'].append(v['ffa_ceiling'])
                site_lineups['ffa_floor'].append(v['ffa_floor'])
                index += 1

        df = pandas.DataFrame(data=site_lineups)
        df.to_csv(local_path)


if __name__ == '__main__':
    main(sys.argv[1:])
    