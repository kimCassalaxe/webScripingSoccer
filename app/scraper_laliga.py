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

def get_laLiga_matchs_of_week():
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
    print("estou aqui 0")
    dados = []
    driver.get(url)
    # tabela recebe os cards de estatistica EX:gols,assists,cleanSheet
    tabelas = WebDriverWait(driver, 15).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.col-12")))[:2]
    #linhas recebe todas as linhas da tabela de classificação
    print("estou aqui 1")
    categorias = tabelas[0].find_elements(By.CSS_SELECTOR,"span.stats-leaderboard__header")
    
    for categoria in categorias:
      print("estou aqui 2")
      # day_matchs recebe a data do jogos
      titulo = categoria.find_element(By.CSS_SELECTOR,"span.match-list__day-date")
      # partidas recebe todas as partidas do day_matchs
      partidas = tabelas[0].find_elements(By.CSS_SELECTOR,"ul.stats-leaderboard__leaderboard")
      
      lista_jogadores = []
      for linha in partidas:
        print("estou aqui")
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
  



  #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cliente API LaLiga - Jogos por Jornada
======================================
Módulo para consultar jogos da LaLiga EA Sports por jornada.

Documentação da API:
https://apim.laliga.com/webview/api/web/subscriptions/laliga-easports-2025/standing?week=19&contentLanguage=en&subscription-key=xxx

Autor: MiniMax Agent
Data: 2026-01-03
"""

import requests
import json
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum


class DiaDaSemana(Enum):
    """Enumeração dos dias da semana em português."""
    SEGUNDA = 0
    TERCA = 1
    QUARTA = 2
    QUINTA = 3
    SEXTA = 4
    SABADO = 5
    DOMINGO = 6


class LaLigaAPIClient:
    """
    Cliente para consumir a API oficial da LaLiga.
    Permite consultar classificação, jogos e estatísticas
    da LaLiga EA Sports por jornada.
    """
    
    # URLs base da API
    BASE_URL = "https://apim.laliga.com"
    
    # Endpoints disponíveis
    ENDPOINTS = {
        "standing": "/webview/api/web/subscriptions/{subscription}/standing",
        "matches": "/webview/api/web/subscriptions/{subscription}/matchs",
        "teams": "/webview/api/web/subscriptions/{subscription}/teams",
        "players": "/webview/api/web/subscriptions/{subscription}/players",
        "top_scorers": "/webview/api/web/subscriptions/{subscription}/topscorers"
    }
    
    def __init__(self, subscription_key: str, subscription: str = "laliga-easports-2025"):
        """
        Inicializa o cliente da API da LaLiga.
        
        Args:
            subscription_key: Chave de assinatura da API
            subscription: Identificador da assinatura (padrão: laliga-easports-2025)
        """
        self.subscription_key = subscription_key
        self.subscription = subscription
        self.session = requests.Session()
        self.session.headers.update({
            "subscription-key": subscription_key,
            "Accept": "application/json",
            "Content-Type": "application/json"
        })
    
    def _make_request(
        self, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Faz uma requisição para a API.
        
        Args:
            endpoint: Endpoint da API
            params: Parâmetros da query string
            
        Returns:
            Dict com a resposta da API
            
        Raises:
            requests.RequestException: Se houver erro na requisição
        """
        url = f"{self.BASE_URL}{endpoint}"
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_classificacao(
        self, 
        week: int, 
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Obtém a classificação da LaLiga para uma jornada específica.
        
        Args:
            week: Número da jornada (1-38)
            language: Idioma do conteúdo (en, es, ca)
            
        Returns:
            Dict com a classificação completa
        """
        endpoint = self.ENDPOINTS["standing"].format(
            subscription=self.subscription
        )
        params = {
            "week": week,
            "contentLanguage": language
        }
        return self._make_request(endpoint, params)
    
    def get_jogos_da_jornada(
        self, 
        week: int, 
        language: str = "en"
    ) -> List[Dict[str, Any]]:
        """
        Obtém todos os jogos de uma jornada específica.
        
        Args:
            week: Número da jornada (1-38)
            language: Idioma do conteúdo (en, es, ca)
            
        Returns:
            Lista de jogos da jornada
        """
        # Primeiro obtemos a classificação que contém os jogos
        classificacao = self.get_classificacao(week, language)
        
        # Extrair jogos da resposta
        # A estrutura pode variar dependendo da API
        jogos = []
        
        if "matchs" in classificacao:
            jogos = classificacao["matchs"]
        elif "matches" in classificacao:
            jogos = classificacao["matches"]
        elif "fixtures" in classificacao:
            jogos = classificacao["fixtures"]
        else:
            # Tentar encontrar jogos em outra estrutura
            jogos = self._extrair_jogos_da_classificacao(classificacao)
        
        return jogos
    
    def _extrair_jogos_da_classificacao(
        self, 
        classificacao: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Extrai jogos de uma resposta de classificação.
        
        Args:
            classificacao: Resposta da API de classificação
            
        Returns:
            Lista de jogos encontrados
        """
        jogos = []
        
        # Procurar em diferentes estruturas possíveis
        if "rounds" in classificacao:
            for round_data in classificacao["rounds"]:
                if "matches" in round_data:
                    jogos.extend(round_data["matches"])
        
        elif "matchday" in classificacao:
            jogos = classificacao["matchday"]
        
        elif "fixtures" in classificacao:
            jogos = classificacao["fixtures"]
        
        return jogos
    
    def get_proxima_jornada(
        self, 
        week_atual: int, 
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Obtém a próxima jornada.
        
        Args:
            week_atual: Jornada atual
            language: Idioma do conteúdo
            
        Returns:
            Dados da próxima jornada
        """
        proxima = week_atual + 1
        if proxima > 38:
            return {"message": "Temporada Finalizada"}
        return self.get_classificacao(proxima, language)
    
    def get_jornada_anterior(
        self, 
        week_atual: int, 
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Obtém a jornada anterior.
        
        Args:
            week_atual: Jornada atual
            language: Idioma do conteúdo
            
        Returns:
            Dados da jornada anterior
        """
        anterior = week_atual - 1
        if anterior < 1:
            return {"message": "Temporada Não Iniciada"}
        return self.get_classificacao(anterior, language)
    
    def get_todas_jornadas(
        self, 
        language: str = "en"
    ) -> List[Dict[str, Any]]:
        """
        Obtém dados de todas as jornadas da temporada.
        
        Args:
            language: Idioma do conteúdo
            
        Returns:
            Lista com dados de todas as jornadas
        """
        todas_jornadas = []
        for week in range(1, 39):
            try:
                dados = self.get_classificacao(week, language)
                todas_jornadas.append({
                    "week": week,
                    "data": dados
                })
            except requests.RequestException as e:
                print(f"Erro ao buscar jornada {week}: {e}")
                continue
        return todas_jornadas
    
    def get_jogos_por_data(
        self, 
        week: int, 
        language: str = "en"
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Organiza os jogos de uma jornada por dia da semana.
        
        Args:
            week: Número da jornada
            language: Idioma do conteúdo
            
        Returns:
            Dict com jogos organizados por dia
        """
        jogos = self.get_jogos_da_jornada(week, language)
        jogos_por_dia = {}
        
        for jogo in jogos:
            data_str = jogo.get("date") or jogo.get("matchDate")
            if data_str:
                try:
                    # Parse da data (formato pode variar)
                    if "T" in data_str:
                        data = datetime.fromisoformat(data_str.replace("Z", "+00:00"))
                    else:
                        data = datetime.strptime(data_str, "%Y-%m-%d")
                    
                    dia_semana = DiaDaSemana(data.weekday()).name
                    
                    if dia_semana not in jogos_por_dia:
                        jogos_por_dia[dia_semana] = []
                    
                    jogos_por_dia[dia_semana].append(jogo)
                except (ValueError, AttributeError):
                    continue
        
        return jogos_por_dia


class FormatadorJogos:
    """Classe para formatar e exibir jogos de forma legível."""
    
    @staticmethod
    def formatar_jogo(jogo: Dict[str, Any]) -> str:
        """
        Formata um único jogo para exibição.
        
        Args:
            jogo: Dados do jogo
            
        Returns:
            String formatada
        """
        equipe_casa = jogo.get("homeTeam", {}).get("name", "TBD")
        equipe_fora = jogo.get("awayTeam", {}).get("name", "TBD")
        placar_casa = jogo.get("score", {}).get("home", "-")
        placar_fora = jogo.get("score", {}).get("away", "-")
        data = jogo.get("date", jogo.get("matchDate", "TBD"))
        
        return f"{equipe_casa} {placar_casa} x {placar_fora} {equipe_fora} | {data}"
    
    @staticmethod
    def formatar_jornada(jogos: List[Dict[str, Any]]) -> str:
        """
        Formata todos os jogos de uma jornada.
        
        Args:
            jogos: Lista de jogos
            
        Returns:
            String formatada com todos os jogos
        """
        if not jogos:
            return "Nenhum jogo encontrado."
        
        linhas = []
        linhas.append("=" * 60)
        linhas.append(f"JORNADA - {len(jogos)} JOGOS")
        linhas.append("=" * 60)
        
        for i, jogo in enumerate(jogos, 1):
            linhas.append(f"{i:2}. {FormatadorJogos.formatar_jogo(jogo)}")
        
        return "\n".join(linhas)
    
    @staticmethod
    def formatar_classificacao(
        classificacao: Dict[str, Any], 
        top_n: int = 10
    ) -> str:
        """
        Formata a tabela de classificação.
        
        Args:
            classificacao: Dados da classificação
            top_n: Quantidade de times a mostrar
            
        Returns:
            String formatada com a classificação
        """
        linhas = []
        linhas.append("=" * 70)
        linhas.append(f"{'POS':^4} | {'TIME':^25} | {'J':^3} | {'V':^3} | {'E':^3} | {'D':^3} | {'GP':^4} | {'GC':^4} | {'PT':^4}")
        linhas.append("=" * 70)
        
        standings = classificacao.get("standings", classificacao.get("table", []))
        
        for i, time in enumerate(standings[:top_n], 1):
            nome = time.get("team", {}).get("shortName", time.get("team", {}).get("name", "TBD"))[:25]
            jogos = time.get("played", time.get("matchesPlayed", 0))
            vitorias = time.get("won", 0)
            empates = time.get("drawn", time.get("draws", 0))
            derrotas = time.get("lost", time.get("losses", 0))
            gp = time.get("goalsFor", time.get("goalsScored", 0))
            gc = time.get("goalsAgainst", time.get("goalsConceded", 0))
            pontos = time.get("points", 0)
            
            linhas.append(f"{i:^4} | {nome:<25} | {jogos:^3} | {vitorias:^3} | {empates:^3} | {derrotas:^3} | {gp:^4} | {gc:^4} | {pontos:^4}")
        
        linhas.append("=" * 70)
        
        return "\n".join(linhas)


def exemplo_uso_completo():
    """
    Exemplo completo de uso do cliente da API LaLiga.
    """
    # Configuração - SUBSTITUA COM SUA CHAVE REAL
    SUBSCRIPTION_KEY = "sua_subscription_key_aqui"
    
    # Inicializar cliente
    cliente = LaLigaAPIClient(
        subscription_key=SUBSCRIPTION_KEY,
        subscription="laliga-easports-2025"
    )
    
    print("=" * 60)
    print("CLIENTE API LALIGA - JOGOS POR JORNADA")
    print("=" * 60)
    
    # Exemplo 1: Obter jogos da jornada 19
    print("\n📅 JORNADA 19:")
    print("-" * 40)
    
    try:
        classificacao_19 = cliente.get_classificacao(week=19, language="en")
        print(f"Status: Sucesso!")
        print(f"Chaves disponíveis: {list(classificacao_19.keys())}")
        
        # Mostrar classificação
        print("\n🏆 CLASSIFICAÇÃO:")
        print(FormatadorJogos.formatar_classificacao(classificacao_19, top_n=5))
        
    except requests.RequestException as e:
        print(f"Erro: {e}")
    
    # Exemplo 2: Obter jogos de várias jornadas
    print("\n📊 JOGOS DE MÚLTIPLAS JORNADAS:")
    print("-" * 40)
    
    for jornada in [1, 10, 19, 38]:
        try:
            dados = cliente.get_classificacao(week=jornada, language="en")
            print(f"Jornada {jornada}: ✓")
        except requests.RequestException as e:
            print(f"Jornada {jornada}: ✗ ({e})")
    
    # Exemplo 3: Obter próxima jornada
    print("\n🔮 PRÓXIMA JORNADA:")
    print("-" * 40)
    
    try:
        proxima = cliente.get_proxima_jornada(week=19, language="en")
        if "message" in proxima:
            print(proxima["message"])
        else:
            print("Dados da próxima jornada disponíveis")
    except requests.RequestException as e:
        print(f"Erro: {e}")


def obter_jogos_exemplo() -> List[Dict[str, Any]]:
    """
    Retorna exemplo de estrutura de dados de jogos
    para demonstração (sem precisar de chave real).
    """
    return [
        {
            "id": "match-001",
            "week": 19,
            "homeTeam": {
                "id": "real-madrid",
                "name": "Real Madrid",
                "shortName": "RMA",
                "crest": "https://.../real-madrid.png"
            },
            "awayTeam": {
                "id": "fc-barcelona",
                "name": "FC Barcelona",
                "shortName": "BAR",
                "crest": "https://.../barcelona.png"
            },
            "score": {
                "home": 2,
                "away": 1
            },
            "date": "2025-01-12T20:00:00Z",
            "venue": "Santiago Bernabéu",
            "status": "FINISHED"
        },
        {
            "id": "match-002",
            "week": 19,
            "homeTeam": {
                "id": "atletico-madrid",
                "name": "Atlético de Madrid",
                "shortName": "ATM",
                "crest": "https://.../atletico.png"
            },
            "awayTeam": {
                "id": "sevilla-fc",
                "name": "Sevilla FC",
                "shortName": "SEV",
                "crest": "https://.../sevilla.png"
            },
            "score": {
                "home": 1,
                "away": 1
            },
            "date": "2025-01-11T17:00:00Z",
            "venue": "Metropolitano",
            "status": "FINISHED"
        },
        {
            "id": "match-003",
            "week": 19,
            "homeTeam": {
                "id": "villarreal",
                "name": "Villarreal CF",
                "shortName": "VIL",
                "crest": "https://.../villarreal.png"
            },
            "awayTeam": {
                "id": "real-sociedad",
                "name": "Real Sociedad",
                "shortName": "RSO",
                "crest": "https://.../real-sociedad.png"
            },
            "score": {
                "home": None,
                "away": None
            },
            "date": "2025-01-12T15:15:00Z",
            "venue": "Estadio de la Cerámica",
            "status": "SCHEDULED"
        }
    ]


def demonstrar_formatacao():
    """
    Demonstra a formatação de jogos (sem API real).
    """
    jogos = obter_jogos_exemplo()
    
    print("=" * 60)
    print("EXEMPLO DE JOGOS - JORNADA 19")
    print("=" * 60)
    
    # Formatar cada jogo
    print("\n📋 LISTA DE JOGOS:")
    for jogo in jogos:
        print(f"  • {FormatadorJogos.formatar_jogo(jogo)}")
    
    # Mostrar detalhes
    print("\n📊 DETALHES DOS JOGOS:")
    for jogo in jogos:
        time_casa = jogo["homeTeam"]["shortName"]
        time_fora = jogo["awayTeam"]["shortName"]
        placar = f"{jogo['score']['home']} x {jogo['score']['away']}" if jogo['score']['home'] else "x"
        estadio = jogo["venue"]
        status = jogo["status"]
        
        print(f"\n  {time_casa} vs {time_fora}")
        print(f"    Placar: {placar}")
        print(f"    Estádio: {estadio}")
        print(f"    Status: {status}")


def criar_script_consulta():
    """
    Cria um script pronto para usar com sua chave real.
    """
    script = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Consulta - Jogos da LaLiga por Jornada
=================================================
"""

import requests

# ⚠️ SUBSTITUA COM SUA CHAVE REAL
SUBSCRIPTION_KEY = "ee7fcd5c543f4485ba2a48856fc7ece9"

def get_classificacao(week: int, language: str = "en") -> dict:
    """Obtém a classificação da LaLiga para uma jornada."""
    url = (
        "https://apim.laliga.com/webview/api/web/subscriptions/"
        "laliga-easports-2025/standing"
    )
    
    params = {
        "week": week,
        "contentLanguage": language
    }
    
    headers = {
        "subscription-key": SUBSCRIPTION_KEY
    }
    
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()


def get_jogos_jornada(week: int) -> list:
    """Extrai os jogos de uma jornada específica."""
    dados = get_classificacao(week)
    
    # A estrutura pode variar, retornar tudo para análise
    return dados


# ========== USO ==========

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Consultar jogos da LaLiga")
    parser.add_argument("--jornada", "-j", type=int, required=True,
                        help="Número da jornada (1-38)")
    parser.add_argument("--idioma", "-i", type=str, default="en",
                        choices=["en", "es", "ca"],
                        help="Idioma do conteúdo")
    
    args = parser.parse_args()
    
    print(f"🔍 Consultando jornada {args.jornada}...")
    dados = get_classificacao(args.jornada, args.idioma)
    print("✅ Sucesso!")
    print(json.dumps(dados, indent=2, ensure_ascii=False))
'''
    
    return script


# ==============================================================================
# EXECUÇÃO PRINCIPAL
# ==============================================================================
"""

if __name__ == "__main__":
    print("=" * 60)
    print("LALIGA API CLIENT - JOGOS POR JORNADA")
    print("=" * 60)
    
    # Demonstrar formatação (sem API real)
    print("\n📝 DEMONSTRAÇÃO DE FORMATAÇÃO")
    print("-" * 40)
    demonstrar_formatacao()
    
    # Gerar script de consulta
    print("\n\n📄 SCRIPT DE CONSULTA PRONTO PARA USO:")
    print("-" * 40)
    script = criar_script_consulta()
    print(script[:500] + "...")
    
    # Salvar script
    with open("consulta_laliga.py", "w", encoding="utf-8") as f:
        f.write(script)
    
    print("\n✅ Script salvo em: consulta_laliga.py")
    print("=" * 60)
"""

