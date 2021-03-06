#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask,jsonify,render_template,request
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, ValidationError, pre_load
from sqlalchemy import desc
from datetime import datetime
from gba import MatchResult
from decimal import Decimal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Password01!@localhost/gba?charset=utf8mb4'
db = SQLAlchemy(app)

class Team(db.Model):
    __tablename__ = 'TEAM'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),unique=True,nullable=False)

    def __repr__(self):
        return '<Team %r>' % self.id

class TeamSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

team_schema = TeamSchema()
teams_schema = TeamSchema(many=True)

class Player(db.Model):
    __tablename__='PLAYER'
    id = db.Column(db.Integer,primary_key=True)
    team_id = db.Column(db.Integer,db.ForeignKey('TEAM.id'),nullable=True)
    name = db.Column(db.String(80),nullable=False)
    salary = db.Column(db.Integer,nullable=True)

    def __init__(self,name,team_id,salary):
        self.name = name
        self.team_id = team_id
        self.salary = salary

    def __repr__(self):
        return '<Player %r>' % self.name

class Match(db.Model):
    __tablename__='MATCH'
    id = db.Column(db.Integer,primary_key=True)
    match_date = db.Column(db.DateTime)
    home_team_id = db.Column(db.Integer,db.ForeignKey('TEAM.id'),nullable=False)
    away_team_id = db.Column(db.Integer,db.ForeignKey('TEAM.id'),nullable=False)
    home_team_score = db.Column(db.Integer)
    away_team_score = db.Column(db.Integer)

    def __init__(self, home_team_id, away_team_id):
        self.home_team_id = home_team_id
        self.away_team_id = away_team_id
        #if match_date is None:
        #    match_date = datetime.utcnow()
        #self.match_date = match_date

#class MatchPlayer(db.Model):
#    __tablename__='MATCH_PLAYER'
  
#class Score(db.Model):
#    __tablename__='SCORE'

class MatchDetail(db.Model):
    __tablename__='MATCH_DETAIL'
    id = db.Column(db.Integer,primary_key=True)
    match_id = db.Column(db.Integer,nullable=False)
    player_id = db.Column(db.Integer, nullable=False)
    foul = db.Column(db.Integer)
    two_point = db.Column(db.Integer)
    three_point = db.Column(db.Integer)
    free_throw = db.Column(db.Integer)

class ScoreBonus(db.Model):
    __tablename__='MATCH_BONUS'
    id = db.Column(db.Integer,primary_key=True)
    team_id = db.Column(db.Integer,db.ForeignKey('TEAM.id'),nullable=False)
    score = db.Column(db.Integer,nullable=False)
    reason = db.Column(db.String(250))

@app.route("/")
def home():
    return "X86黄金联赛(GBA)"

@app.route("/teams",methods=['POST'])
def get_teams():
    teams = Team.query.all()
    result = teams_schema.dump(teams)
    return jsonify({'teams':result.data})

@app.route("/team",methods=['POST'])
def save_team():
    req_data = request.get_json()
    print(req_data)
    team_name = req_data['name']
    team = Team(name=team_name)
    db.session.add(team)
    db.session.commit()
    return "保存成功"

@app.route("/team/test/lemonbar")
def team_clean():
    db.session.query(Team).delete()
    db.session.commit()
    return "clear all team"

@app.route("/match/test/lemonbar")
def match_clean():
    db.session.query(Match).delete()
    db.session.commit()
    return "clear all match"

@app.route("/teams",methods=['GET'])
def get_teams_html():
    teams = Team.query.all()
    return render_template('team.html',teams=teams)

@app.route("/players",methods=['GET'])
def players_list():
    players = Player.query.order_by(Player.team_id).all()
    teams = Team.query.all()
    team_dic = {}
    for team in teams:
        team_dic[team.id]=team.name
    return render_template('players.html',players=players,teams=team_dic)

@app.route("/player",methods=['POST'])
def player_add():
    req_data = request.get_json()
    print(req_data)
    player_name = req_data['name']
    player_team = req_data['team']
    if(player_team == ''):
        player_team = None
        print("team is null")
    salary = req_data['salary']
    player = Player(player_name,player_team,salary)
    db.session.add(player)
    db.session.commit()
    return "保存成功"

@app.route("/player",methods=['GET'])
def player_add_static():
    teams = Team.query.all()
    return render_template('player.html', teams=teams)

@app.route("/match/history",methods=['GET'])
def match_history_load():
    teams = Team.query.all()
    return render_template('match_history.html', teams=teams)

@app.route("/match/bonus",methods=['GET'])
def match_bonus_load():
    teams = Team.query.all()
    return render_template('match_bonus.html', teams=teams)

@app.route("/match/bonus",methods=['POST'])
def match_bonus_add():
    req_data = request.get_json()
    team_id = req_data['team_id']
    score = req_data['score']
    reason = req_data['reason']
    bonus = ScoreBonus(team_id=team_id,score=score,reason=reason)
    db.session.add(bonus)
    db.session.commit()
    return "保存成功"

@app.route("/match/history",methods=['POST'])
def match_history_add():
    req_data = request.get_json()
    print(req_data)
    home_team = req_data['home_team']
    away_team = req_data['away_team']
    home_score = req_data['home_team_score']
    away_score = req_data['away_team_score']
    date = req_data['match_date']
    if(date == ''):
        date = datetime.utcnow()
    match = Match(home_team_id=home_team,away_team_id=away_team)
    match.home_team_score = home_score
    match.away_team_score = away_score
    match.match_date = date
    db.session.add(match)
    db.session.commit()
    return "保存成功"

@app.route("/matches",methods=['GET'])
def matchs_list():
    matches = Match.query.filter(Match.match_date > '2018-08-28').order_by(Match.match_date).all()
    teams = Team.query.all()
    scores = {}
    play_times = {}
    for t in teams:
        play_times[t.id]=0
        scores[t.id]=0

    pre_match_winner_id = None
    pre_match_date = None
    tm = MatchResult(teams)
    for match in matches:
        tm.add_match(match.home_team_id,match.home_team_score,match.away_team_id,match.away_team_score,match.match_date)
        if(match.match_date.day != pre_match_date):
            pre_match_winner_id = None
            pre_match_date = match.match_date.day
            tm.end_add_match()

        #出场次数 begin
        play_times[match.away_team_id] += 1
        if(pre_match_winner_id == None):
            play_times[match.home_team_id] += 1
        #出场次数 end

        if(not scores.has_key(match.home_team_id)):
            scores[match.home_team_id] = 0
        if(not scores.has_key(match.away_team_id)):
            scores[match.away_team_id] = 0
        if(match.home_team_score > match.away_team_score):
            scores[match.home_team_id] += match.home_team_score
            if(match.away_team_score == 0):
                scores[match.home_team_id] += 8
            if(match.away_team_id != 4):
                scores[match.home_team_id] += 4
            scores[match.away_team_id] += match.away_team_score
            if(match.home_team_id == 4):
                scores[match.away_team_id] -= 4
            if(pre_match_winner_id != None and pre_match_winner_id == match.home_team_id and match.away_team_id != 4):
                scores[match.home_team_id] += 4
            pre_match_winner_id = match.home_team_id
        else:
            scores[match.away_team_id] += match.away_team_score
            if(match.home_team_id != 4):
                scores[match.away_team_id] += 4
            if(match.home_team_score == 0):
                scores[match.away_team_id] += 8
            scores[match.home_team_id] += match.home_team_score
            if(match.away_team_id == 4):
                scores[match.home_team_id] -= 4
            pre_match_winner_id = match.away_team_id

    tm.end_add_match()
    #score bonus
    bonus = ScoreBonus.query.all()
    for b in bonus:
        scores[b.team_id] += b.score

    team_views = []
    for t in teams:
        time = Match.query.filter(Match.match_date > '2018-08-28').filter((Match.home_team_id==t.id) | (Match.away_team_id==t.id)).count()
        mv = TeamView(t.name,tm.scores[t.id],time,play_times[t.id],tm.best_inarow[t.id],tm.winners[t.id],tm.losers[t.id],tm.points[t.id],tm.lose_points[t.id],tm.challenge_rejects[t.id])
        team_views.append(mv)

    matches = Match.query.filter(Match.match_date > '2018-08-28').order_by(desc(Match.match_date)).all()
    matches_filter = []
    for m in matches:
        mv = MatchView(m.home_team_id,m.away_team_id,m.match_date.strftime("%Y-%m-%d"),m.home_team_score,m.away_team_score)
        matches_filter.append(mv)
    team_dic = {}
    for team in teams:
        team_dic[team.id]=team.name
    return render_template('matches.html', matches=matches_filter,teams=team_dic,scores=team_views)

@app.route("/matches/history",methods=['GET'])
def matchs_list_history():
    matches = Match.query.filter(Match.match_date < '2018-08-28').order_by(Match.match_date).all()
    teams = Team.query.all()
    scores = {}
    play_times = {}
    for t in teams:
        play_times[t.id]=0
        scores[t.id]=0

    pre_match_winner_id = None
    pre_match_date = None
    tm = MatchResult(teams)
    for match in matches:
        tm.add_match(match.home_team_id,match.home_team_score,match.away_team_id,match.away_team_score,match.match_date)
        if(match.match_date.day != pre_match_date):
            pre_match_winner_id = None
            pre_match_date = match.match_date.day
            tm.end_add_match()

        #出场次数 begin
        play_times[match.away_team_id] += 1
        if(pre_match_winner_id == None):
            play_times[match.home_team_id] += 1
        #出场次数 end

        if(not scores.has_key(match.home_team_id)):
            scores[match.home_team_id] = 0
        if(not scores.has_key(match.away_team_id)):
            scores[match.away_team_id] = 0
        if(match.home_team_score > match.away_team_score):
            scores[match.home_team_id] += match.home_team_score
            if(match.away_team_score == 0):
                scores[match.home_team_id] += 8
            if(match.away_team_id != 4):
                scores[match.home_team_id] += 4
            scores[match.away_team_id] += match.away_team_score
            if(match.home_team_id == 4):
                scores[match.away_team_id] -= 4
            if(pre_match_winner_id != None and pre_match_winner_id == match.home_team_id and match.away_team_id != 4):
                scores[match.home_team_id] += 4
            pre_match_winner_id = match.home_team_id
        else:
            scores[match.away_team_id] += match.away_team_score
            if(match.home_team_id != 4):
                scores[match.away_team_id] += 4
            if(match.home_team_score == 0):
                scores[match.away_team_id] += 8
            scores[match.home_team_id] += match.home_team_score
            if(match.away_team_id == 4):
                scores[match.home_team_id] -= 4
            pre_match_winner_id = match.away_team_id

    tm.end_add_match()
    #score bonus
    bonus = ScoreBonus.query.all()
    for b in bonus:
        scores[b.team_id] += b.score

    team_views = []
    for t in teams:
        time = Match.query.filter(Match.match_date < '2018-08-28').filter((Match.home_team_id==t.id) | (Match.away_team_id==t.id)).count()
        sc = scores[t.id]
        mv = TeamView(t.name,sc,time,play_times[t.id],tm.best_inarow[t.id],tm.winners[t.id],tm.losers[t.id],tm.points[t.id],tm.lose_points[t.id],tm.challenge_rejects[t.id])
        team_views.append(mv)

    matches = Match.query.filter(Match.match_date < '2018-08-28').order_by(desc(Match.match_date)).all()
    matches_filter = []
    for m in matches:
        mv = MatchView(m.home_team_id,m.away_team_id,m.match_date.strftime("%Y-%m-%d"),m.home_team_score,m.away_team_score)
        matches_filter.append(mv)
    team_dic = {}
    for team in teams:
        team_dic[team.id]=team.name
    return render_template('matches_history.html', matches=matches_filter,teams=team_dic,scores=team_views)

class MatchView:
    def __init__(self,home_id,away_id,date,home_score,away_score):
        self.home_team_id=home_id
        self.away_team_id=away_id
        self.match_date=date
        self.home_team_score=home_score
        self.away_team_score=away_score

class TeamView:
    def __init__(self,team_name,team_score,team_times,play_times,best_inarow,winners,losers,points,lose_points,challenge_rejects):
        self.name = team_name
        self.score = team_score
        self.times = team_times
        self.play_times = play_times
        self.best_inarow = best_inarow
        self.winners = winners
        self.losers = losers
        self.points = points
        self.lose_points = lose_points
        if (team_times > 0):
            self.points_per_match = Decimal(float(points)/float(team_times)).quantize(Decimal('0.00'))
            self.lose_points_per_match = Decimal(float(lose_points)/float(team_times)).quantize(Decimal('0.00'))
        self.challenge_rejects = challenge_rejects

db.create_all()
