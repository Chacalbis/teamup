#!/usr/bin/python
import argparse, yaml, sys
from itertools import combinations

last_best = 100000000000


def unique_group(iterable, k, n, groups=0):
    if groups == k:
        yield []
    pool = set(iterable)
    for combination in combinations(pool, n):
        for rest in unique_group(pool.difference(combination), k, n, groups + 1):
            yield [combination, *rest]

def weightedSkill(technicalNote, enduranceNote, goalNote, teamsize):
    return round((teamsize * (technicalNote + enduranceNote) + goalNote) / (teamsize * 2 + 1), 1)


def gap(groups):
    total_skills = [sum(player_skills[player] for player in group) for group in groups]
    return round(total_skills[0] - total_skills[1], 1)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Optimize teams based on linear programming.")
    parser.add_argument('-p', '--players', required=True, action='store',
            type=str, help="The yaml player file.")
    parser.add_argument('-k', '--numteams', required=True, action='store',
            type=int, help="The number of teams.")
    parser.add_argument('-n', '--teamsize', required=True, action='store',
            type=int, help="The size of the teams.")
    args = parser.parse_args()

    players = yaml.load(open(args.players, 'rt'), Loader=yaml.FullLoader)

    players = sorted(players, key=lambda k: weightedSkill(k['technicalNote'], k['enduranceNote'], k['goalNote'], args.teamsize))

    player_skills = {player['name']: weightedSkill(player['technicalNote'], player['enduranceNote'], player['goalNote'], args.teamsize) for player in players}
    print(player_skills)

    i = 0
    for grouping in unique_group(player_skills, args.numteams, args.teamsize):
        i += 1
        if i % 100000 == 0:
            sys.stdout.write('.')
            sys.stdout.flush()
        if gap(grouping) < last_best:
            last_best = gap(grouping)
            print("")
            print(f"Ecart: {gap(grouping)}")
            print("============")
            print(grouping)
            print("============")
