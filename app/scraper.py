import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

from .database import Dados
from datetime import date
def get_matchs_of_week():
  #url para obter os jogos da premier league de uma semana específica
  url = "https://www.premierleague.com/en/matches?competition=8&season=2025&matchweek=17&month=12"
  options = Options()
  options.add_argument("--headless")
  options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
  )
  driver = webdriver.Firefox(options=options)
  try:
    dados = []
    driver.get(url)
    # tabela recebe a tabela de classificação da Premier League
    tabela = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.match-list")))
    #linhas recebe todas as linhas da tabela de classificação
    linhas = tabela.find_elements(By.CSS_SELECTOR,"div.match-list__day-matches")
    print(len(linhas))

    print("#"*50)
    for dia in linhas:
      # day_matchs recebe a data do jogos
      day_matchs = dia.find_element(By.CSS_SELECTOR,"span.match-list__day-date").get_attribute("innerText") 
      # partidas recebe todas as partidas do day_matchs
      partidas = dia.find_elements(By.CSS_SELECTOR,"a.match-card")
      
      jogos = []
      for linha in partidas:
        #pegar os nomes das equipes do jogo
        times = linha.find_elements(By.CSS_SELECTOR,"span.match-card__team-name--full")
        #pegar os logos das equipes do jogo
        logos = linha.find_elements(By.CSS_SELECTOR,"img.club-badge__img")
        home_time = times[0].get_attribute("innerText")
        home_time_logo = logos[0].get_attribute("src")
        away_time = times[1].get_attribute("innerText")
        away_time_logo = logos[1].get_attribute("src")
        time_to_start = 0
        try:
          time_to_start = linha.find_element(By.CSS_SELECTOR,"span.match-card__score-label").get_attribute("innerText") 
        except Exception as e:
          time_to_start = linha.find_element(By.CSS_SELECTOR,"span.match-card__kickoff-time").get_attribute("innerText")
        jogos.append({
          "equipe_casa": home_time,
          "equipe_casa_logo": home_time_logo,
          "equipe_fora": away_time,
          "equipe_fora_logo": away_time_logo,
          "horario": time_to_start,
        })

      dados.append({
        day_matchs:jogos
      })

    if len(dados) > 0 :
      Dados['ligas']['Premier_League']['jornada'] = dados 
      return dados
    else:
      print("Nenhum jogo encontrado para a semana especificada.")
  except Exception as e:
    print(e)
  finally:
    driver.quit()
  
def get_statistic():
  #url para obter os jogos da premier league de uma semana específica
  url = "https://www.premierleague.com/en/stats"
  options = Options()
  options.add_argument("--headless")
  options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
  )
  driver = webdriver.Firefox(options=options)
  try:
    dados = []
    driver.get(url)
    # tabela recebe os cards de estatistica EX:gols,assists,cleanSheet
    tabelas = WebDriverWait(driver, 15).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.col-12")))[:2]
    #linhas recebe todas as linhas da tabela de classificação
    print("#"*50)
    print(tabelas[0].get_attribute("outerHTML"))
    print("_"*50)
    categorias = tabelas[0].find_elements(By.CSS_SELECTOR,"span.stats-leaderboard__header")
    
    print(len(categorias))
    print("#"*50)
    for categoria in categorias:
      print(categoria.get_attribute("outerHTML"))
      # day_matchs recebe a data do jogos
      titulo = categoria.find_element(By.CSS_SELECTOR,"span.match-list__day-date")
      # partidas recebe todas as partidas do day_matchs
      partidas = tabelas[0].find_elements(By.CSS_SELECTOR,"ul.stats-leaderboard__leaderboard")
      
      lista_jogadores = []
      for linha in partidas:
        #pegar os nomes das equipes do jogo
        pos = linha.find_element(By.CSS_SELECTOR,"span.stats-leaderboard__pos")
        #pegar os logos das equipes do jogo
        nome = linha.find_element(By.CSS_SELECTOR,"span.stats-leaderboard__name").get_attribute("innerText")
        avatar = linha.find_element(By.CSS_SELECTOR,"img").get_attribute("src")
        club = {
          "logo":linha.find_element(By.CSS_SELECTOR,"img.club-badge__img").get_attribute("src"),"nome":linha.find_element(By.CSS_SELECTOR,"span.stats-leaderboard__team-name u-show-desktop").get_attribute("innerText")
        }
        valor = linha.find_element(By.CSS_SELECTOR,"span.stats-leaderboard__stat-value").get_attribute("innerText")
        lista_jogadores.append({
          "posicao": pos,
          "nome": nome,
          "avatar": avatar,
          "clube": club,
          "valor": valor,
        })

      dados.append({
        titulo: lista_jogadores
      })

    if len(dados) > 0 :
      Dados['ligas']['Premier_League']['estatistica'] = dados 
      return dados
    else:
      print("Nenhum jogo encontrado para a semana especificada.")
  except Exception as e:
    print(e)
  finally:
    driver.quit()
  



def get_premier_league_data():
  print("Coletando dados da Premier League...")
  url = "https://www.premierleague.com/en/tables?competition=8"

  options = Options()
  options.add_argument("--headless")
  options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
  )
  driver = webdriver.Firefox(options=options)
  try:
    dados = []
    driver.get(url)
    # tabela recebe a tabela de classificação da Premier League
    tabela = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "tbody.standings-table__table-body")))
    #linhas recebe todas as linhas da tabela de classificação
    linhas = tabela.find_elements(By.CSS_SELECTOR,"tr.standings-row")
    for linha in linhas:
      gols_pro = int(linha.find_element(By.CSS_SELECTOR,"div.standings-row__stat--goals-for").get_attribute("innerText"))
      gols_contra = int(linha.find_element(By.CSS_SELECTOR,"div.standings-row__stat--goals-against").get_attribute("innerText"))
      gols_dif = gols_pro - gols_contra
      dados.append({
        "posicao": linha.find_element(By.CSS_SELECTOR,"div.standings-row__position").get_attribute("innerText"),
        "time": linha.find_element(By.CSS_SELECTOR,"span.standings-row__team-name-long").get_attribute("innerText"),
        "jogos": linha.find_element(By.CSS_SELECTOR,"div.standings-row__stat--played").get_attribute("innerText"),
        "pontos": linha.find_element(By.CSS_SELECTOR,"div.standings-row__stat--points").get_attribute("innerText"),
        "vitorias": linha.find_element(By.CSS_SELECTOR,"div.standings-row__stat--won").get_attribute("innerText"),
        "empates": linha.find_element(By.CSS_SELECTOR,"div.standings-row__stat--drawn").get_attribute("innerText"),
        "derrotas": linha.find_element(By.CSS_SELECTOR,"div.standings-row__stat--lost").get_attribute("innerText"),
        "gols_pro": gols_pro,
        "gols_contra": gols_contra,
        "saldo_gols": gols_dif,
        "logo": linha.find_element(By.CSS_SELECTOR,"img.club-badge__img").get_attribute("src"),
      })
    Dados['ligas']['Premier_League']['clasificacao'] = dados
  except Exception as e:
    print(e)
  finally:
    driver.quit()
  