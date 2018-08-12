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

class MatchWinnersTestCase(TeamMatchTestCase):
    def test_winners_time(self):
        tm = MatchResult(self.teams)
        tm.add_match(0,7,1,4)
        tm.add_match(0,7,2,3)
        self.assertEqual(tm.winners[0],2,'team 0 winners 2 matches')
        self.assertEqual(tm.winners[1],0,'team 1 winners 0 matches')
        self.assertEqual(tm.losers[1],1,'team 1 losers 1 matches')
        self.assertEqual(tm.winners[2],0,'team 2 winners 0 matches')
        self.assertEqual(tm.losers[2],1,'team 2 losers 1 matches')

if __name__ == '__main__':
    unittest.main()
