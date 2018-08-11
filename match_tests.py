#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from gba import MatchResult,Team

class TeamMatchTestCase(unittest.TestCase):
    def setUp(self):
        self.teams = []
        self.teams.append(Team(0,'team0'))
        self.teams.append(Team(1,'team1'))
        self.teams.append(Team(2,'team2'))
       

class MatchWinInarowTestCase(TeamMatchTestCase):
    def test_win_inarow(self):
        tm = MatchResult(self.teams)
        self.assertTrue(tm.win_inarow.has_key(0))
        tm.add_match(0,5,1,7)
        tm.add_match(1,7,2,3)
        tm.end_add_match()
        self.assertEqual(tm.best_inarow[1],2,'team 1 win 2 in a row')
        self.assertEqual(tm.best_inarow[0],0,'team 0 win 0 in a row')

if __name__ == '__main__':
    unittest.main()
