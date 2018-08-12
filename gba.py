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
        self.clear()
        for team in self.teams:
            self.winners[team.id] = 0
            self.losers[team.id] = 0
            self.points[team.id] = 0
            self.lose_points[team.id] = 0
            self.challenge_rejects[team.id] = 0

    def add_match(self, home_id, home_score, away_id, away_score):
        self.points[home_id] += home_score
        self.lose_points[home_id] += away_score
        self.lose_points[away_id] += home_score
        self.points[away_id] += away_score
        if(home_score > away_score):#主场赢球
            self.win_inarow[home_id] += 1
            self.winners[home_id] += 1
            self.losers[away_id] += 1
            self.challenge_rejects[away_id] += 1
        else:#客场赢球
            self.win_inarow[away_id] = 1
            self.winners[away_id] += 1
            self.losers[home_id] += 1
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
