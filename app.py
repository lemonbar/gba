#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, ValidationError, pre_load

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
    team_id = db.Column(db.Integer,nullable=True)
    name = db.Column(db.String(80),nullable=False)
    salary = db.Column(db.Integer,nullable=True)
    #create_date
    #update_date

class Match(db.Model):
    __tablename__='MATCH'
    id = db.Column(db.Integer,primary_key=True)
    #match_date
    home_team_id = db.Column(db.Integer,nullable=False)
    away_team_id = db.Column(db.Integer,nullable=False)
    #home_team_score
    #away_team_score

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

@app.route("/teams")
def get_teams():
    teams = Team.query.all()
    result = teams_schema.dump(teams)
    return jsonify({'teams':result.data})

db.create_all()
