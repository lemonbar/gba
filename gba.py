#!/usr/bin/env python
# -*- coding: utf-8 -*-

class MatchResult:

    def __init__(self, teams):
        self.win_inarow = {}
        self.best_inarow = {}
        self.teams = teams
        self.clear()

    def add_match(self, home_id, home_score, away_id, away_score):
        if(home_score > away_score):#主场赢球
            self.win_inarow[home_id] += 1
        else:#客场赢球
            self.win_inarow[away_id] = 1
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
