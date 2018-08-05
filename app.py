#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask,jsonify,render_template,request
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, ValidationError, pre_load
from datetime import datetime

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
    players = Player.query.all()
    return render_template('player.html',players=players)

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

@app.route("/match/history",methods=['GET'])
def match_history_load():
    teams = Team.query.all()
    return render_template('match_history.html', teams=teams)

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
    matches = Match.query.order_by(Match.match_date).all()
    teams = Team.query.all()
    scores = {}
    pre_match_winner_id = None
    for match in matches:
        if(not scores.has_key(match.home_team_id)):
            scores[match.home_team_id] = 0
        if(not scores.has_key(match.away_team_id)):
            scores[match.away_team_id] = 0
        if(match.home_team_score > match.away_team_score):
            scores[match.home_team_id] += match.home_team_score
            scores[match.home_team_id] += 4
            scores[match.away_team_id] += match.away_team_score
            if(match.home_team_id == 4):
                scores[match.away_team_id] -= 4
            if(pre_match_winner_id != None and pre_match_winner_id == match.home_team_id):
                scores[match.home_team_id] += 4
            pre_match_winner_id = match.home_team_id
        else:
            scores[match.away_team_id] += match.away_team_score
            scores[match.away_team_id] += 4
            scores[match.home_team_id] += match.home_team_score
            if(match.away_team_id == 4):
                scores[match.home_team_id] -= 4
            pre_match_winner_id = match.away_team_id

    team_dic = {}
    for team in teams:
        team_dic[team.id]=team.name
    return render_template('matches.html', matches=matches,teams=team_dic,scores=scores)

db.create_all()
