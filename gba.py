#!/usr/bin/env python
# -*- coding: utf-8 -*-

class MatchResult:

    def __init__(self, teams):
        self.win_inarow = {}
        self.best_inarow = {}
        self.winners = {}
        self.losers = {}
        self.teams = teams
        self.points = {}
        self.lose_points = {}
        self.challenge_rejects = {}
        self.scores = {}
        self.pre_match_date = None
        self.pre_match_winner = None
        self.clear()
        for team in self.teams:
            self.winners[team.id] = 0
            self.losers[team.id] = 0
            self.points[team.id] = 0
            self.scores[team.id] = 0
            self.lose_points[team.id] = 0
            self.challenge_rejects[team.id] = 0

    def add_match(self, home_id, home_score, away_id, away_score, match_date):
        if(match_date != self.pre_match_date):
	    self.pre_match_date = match_date
            self.pre_match_winner = None
        self.points[home_id] += home_score
        self.lose_points[home_id] += away_score
        self.lose_points[away_id] += home_score
        self.points[away_id] += away_score
        if(home_score > away_score):#主场赢球
            self.win_inarow[home_id] += 1
            self.winners[home_id] += 1
            self.scores[home_id] += (home_score + 3)
            self.scores[away_id] += (away_score)
            self.losers[away_id] += 1
            self.challenge_rejects[away_id] += 1
            if(self.pre_match_winner == home_id):
                self.scores[home_id] += 3
            if(away_score == 0):
                self.scores[home_id] += 6
            self.pre_match_winner = home_id
        else:#客场赢球
            self.win_inarow[away_id] = 1
            self.winners[away_id] += 1
            self.scores[home_id] += (home_score)
            self.scores[away_id] += (away_score + 3)
            self.losers[home_id] += 1
            if(self.pre_match_winner == away_id):
                self.scores[away_id] += 3
            if(home_score == 0):
                self.scores[away_id] += 6
            self.pre_match_winner = away_id
            if((self.best_inarow.has_key(home_id) and self.best_inarow[home_id] < self.win_inarow[home_id]) or (not self.best_inarow.has_key(home_id))):
                self.best_inarow[home_id] = self.win_inarow[home_id]

    def end_add_match(self):
        for key in self.win_inarow:
            if((self.best_inarow.has_key(key) and self.best_inarow[key] < self.win_inarow[key]) or (not self.best_inarow.has_key(key))):
                self.best_inarow[key] = self.win_inarow[key]
        self.clear()

    def clear(self):
        for team in self.teams:
            self.win_inarow[team.id] = 0

class Team:
    def __init__(self, id, name):
        self.id = id
        self.name = name
