
from flask import Blueprint, jsonify
from .database import Dados
from .scraper import *

main = Blueprint('main', __name__)

@main.route('/api/')
def index():
  return jsonify({
    "message": "API rodando com sucesso 🚀",
    "dados": Dados
    }) 


@main.route('/api/ligas')
def ligas():
  return jsonify({"message": "ligas ","date":Dados["ligas"]})

@main.route('/api/ligas/la_liga')
def la_liga():
  return jsonify({"message": "la_liga 🚀"})

@main.route('/api/ligas/la_liga/tabel')
def la_liga_tabela():
  return jsonify({"message": "la_liga tabela"})

@main.route('/api/ligas/la_liga/jogos_hoje')
def la_liga_jogos_hoje():
  return jsonify({"message": "la_liga jogos_hoje"})

@main.route('/api/ligas/serie_a')
def serie_a():
  return jsonify({"message": "serie_a 🚀"})

@main.route('/api/ligas/premier_league')
def premier_league():
  dados = Dados['ligas']['Premier_League']
  return jsonify({"message": "premier_league 🚀","date":dados})

@main.route('/api/ligas/premier_league/matchsweek/<week>/<month>/<year>')
# rota para obter os jogos da premier league de uma semana específica
# ex: /api/ligas/premier_league/matchsweek/18/12/2025
def premier_league_matches(week, month, year):
  matchs = get_matchs_of_week(week, month, year)

  return jsonify({"message": "jogos da premier_league "if matchs else "nenhum jogo encontrado","date":matchs})
# url = str(f"https://www.premierleague.com/en/matches?competition=8&season={year}&matchweek={week}&month={month}")

@main.route('/api/ligas/premier_league/statistic')
# rota para obter as estatisticas da premier league
def premier_league_statistics():
  dados = get_statistic()

  return jsonify({"message": "estatistica da premier_league!!!"if dados else "nenhum dado encontrado","date":dados})
# url = str(f"https://www.premierleague.com/en/matches?competition=8&season={year}&matchweek={week}&month={month}")

@main.route('/api/ligas/bundesliga')
def bundesliga():
  return jsonify({"message": "bundesliga 🚀"} )


@main.route('/api/ligas/ligue_1')
def ligue_1():
  return jsonify({"message": "ligue_1 🚀"})

@main.route('/api/ligas/eredivisie')
def eredivisie():
  return jsonify({"message": "eredivisie 🚀"})