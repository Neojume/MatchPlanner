#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 04 12:13:06 2013

@author: Steven
"""
from copy import deepcopy
from random import shuffle, choice

def scheme_score(scheme, players, tradeoff=0.5):
    '''
    Calculates the score of the given scheme. This score discounts schemes that
    let players play often in a row.
    '''

    score = 0
    play_streak = 0
    wait_streak = 0
    play_counter = dict()
    wait_counter = dict()

    for player in players:
        play_counter[player] = 0
        wait_counter[player] = 0

    for playing_round in scheme:
        # Get the players in the round
        current_players = []
        for p1, p2 in playing_round:
            current_players.append(p1)
            current_players.append(p2)

        for player in players:
            if player in current_players:
                play_counter[player] += 1

                score += (1.0 - tradeoff) * wait_counter[player] ** 2
                if wait_counter[player] > wait_streak:
                    wait_streak = wait_counter[player]
                wait_counter[player] = 0
            else:
                wait_counter[player] += 1

                score += tradeoff * play_counter[player] ** 2
                if play_counter[player] > play_streak:
                    play_streak = play_counter[player]
                play_counter[player] = 0

    for player in players:
        if player in current_players:
            play_counter[player] += 1

            score += (1.0 - tradeoff) * wait_counter[player] ** 2
            if wait_counter[player] > wait_streak:
                wait_streak = wait_counter[player]
            wait_counter[player] = 0
        else:
            wait_counter[player] += 1

            score += tradeoff * play_counter[player] ** 2
            if play_counter[player] > play_streak:
                play_streak = play_counter[player]
            play_counter[player] = 0

    return score, play_streak, wait_streak

def random_scheme(tmp_scheme, matches):
    '''
    Creates a playing schedule by shuffling the matches.
    '''

    stack = []

    shuffle(matches)
    tmp_matches = matches

    while len(tmp_matches) > 0:
        current_round = tmp_scheme[-1]

        if len(current_round) < tables:
            # Get players in current round
            current_players = []
            for p1, p2 in current_round:
                current_players.append(p1)
                current_players.append(p2)

            none_possible = True

            for p1, p2 in tmp_matches:
                if (p1 not in current_players) and (p2 not in current_players):
                    new_scheme = deepcopy(tmp_scheme)
                    new_scheme[-1].append((p1, p2))
                    new_matches = list(tmp_matches)
                    new_matches.remove((p1, p2))
                    stack.append((new_matches, new_scheme))
                    none_possible = False

            if none_possible:
                tmp_scheme[-1].append((None,None))
                stack.append((tmp_matches, tmp_scheme))
        else:
            # Create a new round
            tmp_scheme.append([])
            stack.append((tmp_matches, tmp_scheme))

        tmp_matches, tmp_scheme = stack.pop()
    return tmp_scheme

def print_scheme(scheme, players):

    plays = dict()
    waits = dict()

    max_plays = dict()
    max_waits = dict()

    for player in players:
        plays[player] = 0
        waits[player] = 0

        max_plays[player] = 0
        max_waits[player] = 0

    for playing_round in scheme:
        print playing_round

        current_players = []
        for p1,p2 in playing_round:
            current_players.append(p1)
            current_players.append(p2)

        for player in players:
            if player in current_players:
                plays[player] += 1
                max_waits[player] = max(waits[player], max_waits[player])
                waits[player] = 0
            else:
                waits[player] += 1
                max_plays[player] = max(plays[player], max_plays[player])
                plays[player] = 0

    print 'max plays/waits per player'

    for player in players:
        print '%s: %d / %d' % (player,max_plays[player], max_waits[player])

def rand_swap((X,Y)):
    return choice([(X,Y), (Y,X)])


if __name__ == '__main__':

    # Get all info
    matchup_twice =  (raw_input('Matchup twice? (yes/no)\n>>') == 'yes')

    tradeoff = float(raw_input('Play/wait tradeoff (between 0 and 1)\n (0 = dont care about long play streaks, 1 = dont care about wait streaks)\n>>'))

    print 'Input players, type stop to stop'
    players = []
    matches = []

    while 1:
        player = raw_input('>>')
        if player == 'stop':
            break

        for other_player in players:
            matches.append((player, other_player))

            if matchup_twice:
                matches.append((other_player, player))

        players.append(player)

    tables = int(raw_input('Number of playingfields?\n>>'))

    if not matchup_twice:
        # If there are an even number of matched to be played for each player
        # perfect balance is possible
        perfect_balance =  ((len(players) - 1) % 2 == 0)

        balanced = False
        while not balanced:
            # Swap at random and evaluate the balance
            matches = map(rand_swap, matches)

            starts = dict()

            for player in players:
                starts[player] = 0

            for match in matches:
                starts[match[0]] += 1

            sorted_starts = sorted(starts.values())
            diff =  abs(sorted_starts[0] - sorted_starts[-1])

            if perfect_balance:
                balanced = (diff == 0)
            else:
                balanced = (diff < 2)

        for pair in starts.iteritems():
            print pair

    tries = 1

    scheme = random_scheme([[]], matches)
    tmp_scheme = [scheme[0]]

    for match in scheme[0]:
        matches.remove(match)
    tmp_scheme = [scheme[0]]

    best_score, best_play_streak, best_wait_streak = scheme_score(scheme, players)
    best_length = len(scheme)

    try:
        while 1:
            tries += 1

            if tries % 1000 == 0:
                print 'Looked at', tries, 'schemes'

            scheme = random_scheme(tmp_scheme, matches)
            score, play_streak, wait_streak = scheme_score(scheme, players)

            #if len(scheme) > best_length:
            #    continue

            if  score < best_score:
                best_scheme = scheme
                best_length = len(scheme)
                best_play_streak = play_streak
                best_wait_streak = wait_streak
                best_score = score

                print_scheme(scheme, players)

                print 'Longest play/wait streaks: %d / %d' % (play_streak, wait_streak)
                print 'Score:', score
                print 'Looked at %d schemes' % tries
    except KeyboardInterrupt:
        # Print the scheme
        print 'Best of %d tries:' % tries
        print_scheme(best_scheme, players)
