#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 04 12:13:06 2013

@author: Steven
"""


def get_matches(players, matchup_twice):
    matches = []
    for i, player_a in enumerate(players):
        for j, player_b in enumerate(players):
            if i == j:
                continue

            if not matchup_twice and j > i:
                continue

            # Balance who goes first for matchup once
            if not matchup_twice and (i + j) & 1:
                matches.append((player_b, player_a))
            else:
                matches.append((player_a, player_b))

    return matches


def create_schema(players, fields, matchup_twice):

    def quadratic(x):
        return x * x

    def best_next_match(partial_round):
        worst_score = quadratic(len(players) * 2)

        players_in_current_round = list(sum(partial_round, ()))  # Fast way to flatten list of tuples

        # Lower is better
        player_scores = {
            player: quadratic(play_penalty[player]) - len(matches_for_player[player]) + (worst_score * (player in players_in_current_round))
            for player in matches_for_player
        }
        # Lower is better
        match_scores = {
            match: player_scores[match[0]] + player_scores[match[1]]
            for match in matches
        }

        best_score = worst_score
        best_match = None

        for match, score in match_scores.items():
            if score < best_score:
                best_match = match
                best_score = score

        return best_match

    max_penalty = len(players) - 1
    play_penalty = {
        player: max_penalty
        for player in players
    }

    matches = get_matches(players, matchup_twice)

    matches_for_player = {
        player: [match for match in matches if player in match]
        for player in players
    }

    rounds = []

    while matches:
        current_round = []

        for _ in range(fields):
            match = best_next_match(current_round)

            # There is no possible game anymore for this round
            if match is None:
                continue

            # Otherwise update everything
            current_round.append(match)
            matches.remove(match)

            player_a, player_b = match
            matches_for_player[player_a].remove(match)
            matches_for_player[player_b].remove(match)

            play_penalty[player_a] = max_penalty
            play_penalty[player_b] = max_penalty

        for player in players:
            play_penalty[player] -= 1

        rounds.append(current_round)

    return rounds


def print_scheme(scheme, players):

    play_streak = dict()
    wait_streak = dict()

    for player in players:
        play_streak[player] = [0]
        wait_streak[player] = [0]

    for i, playing_round in enumerate(scheme):
        players_in_current_round = list(sum(playing_round, ()))  # Fast way to flatten list of tuples
        print(str(i + 1) + " " + "\t".join(players_in_current_round))

    for playing_round in scheme:
        # Get the players in the round
        current_players = list(sum(playing_round, ()))  # Fast way to flatten list of tuples

        for player in players:
            if player in current_players:
                play_streak[player].append(play_streak[player][-1] + 1)
                wait_streak[player].append(0)
            else:
                play_streak[player].append(0)
                wait_streak[player].append(wait_streak[player][-1] + 1)

    print 'max plays/waits per player'

    for player in players:
        print '%s: %d / %d' % (player, max(play_streak[player]), max(wait_streak[player]))


if __name__ == '__main__':

    print 'Input players, type stop to stop'
    players = []
    matches = []

    while True:
        player = raw_input('>>')

        if player == 'stop':
            break

        players.append(player)

    fields = int(raw_input('Number of playingfields?\n>>'))
    matchup_twice = (raw_input('Matchup twice? (yes/no)\n>>') == 'yes')

    s = create_schema(players, fields, matchup_twice)
    print(s)
    print_scheme(s, players)

