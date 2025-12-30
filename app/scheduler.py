from apscheduler.schedulers.background import BackgroundScheduler
from .scraper import get_premier_league_data
from .scraper import get_matchs_of_week
from .database import atualizar_premier_league

def atualizar_dados():
  get_premier_league_data()
  get_matchs_of_week()
  

def start_scheduler():
  print("-"*20,"Iniciando o agendador de tarefas...","-"*20)
  scheduler = BackgroundScheduler()
  #scheduler.add_job(atualizar_dados,"interval",hours=15)
  #scheduler.start()
  #atualizar_dados()