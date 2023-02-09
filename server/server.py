from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests
import re
import html
from codecs import encode, decode

source = requests.get("https://www.cbssports.com/nba/teams/GS/golden-state-warriors/").text
soup = BeautifulSoup(source, 'lxml')
gsw_standing = soup.find("aside", class_="PageTitle-description").text.strip().split("-")[-1].strip()
gsw_wl = soup.find("aside", class_="PageTitle-description").text.strip().split("|")[0].split(" ")[0]

source2 = requests.get("https://sports.yahoo.com/nba/teams/golden-state/").text
soup2 = BeautifulSoup(source2, 'lxml')
gsw_raw_rankings = soup2.find("div", class_="ys-player-header").getText().split("|")[1]
gsw_rankings = re.findall(r"(\d+)th", gsw_raw_rankings)
gsw_ranking_numbers = re.findall(r"th(\d+\.?\d*)", gsw_raw_rankings)
gsw_ranking_titles = ["Field Goal%", "3-point%", "Points Scored", "Total Rebounds"]
gsw_ranking_units = ["FG%", "3P%", "PPG", "RPG"]

source3 = requests.get("https://www.basketball-reference.com/teams/GSW/2023_games.html").text
soup3 = BeautifulSoup(source3, 'lxml')
gsw_meta = soup3.find(id="meta").findChildren()
gsw_last_game_link = "https://www.basketball-reference.com"
gsw_last_game_table = ""
gsw_last_game_opponent_table = ""
for i, child in enumerate(gsw_meta):
    if i == 17:
        gsw_last_game_link += child.find("a")["href"]
    if i == 19:
        gsw_opponent = child.text.strip().split()[-1]
        gsw_last_game = ' '.join(child.text.strip().split())
    if i == 20:
        gsw_next_game = ' '.join(child.text.strip().split()[2:])
if gsw_last_game_link != "https://www.basketball-reference.com":
    source4 = requests.get(gsw_last_game_link).text
    soup4 = BeautifulSoup(source4, 'lxml')
    gsw_last_game_meta = str(soup4.find(id="box-GSW-game-basic").prettify()).split("\n")
    gsw_last_game_opponent_meta = str(soup4.find(id="box-" + gsw_opponent + "-game-basic").prettify()).split("\n")
    i = 0
    while i < len(gsw_last_game_meta):
        if i < 1 or i > 3:
            if "over_header" in gsw_last_game_meta[i]:
                i += 8
                continue
            if not gsw_last_game_meta[i].strip().startswith("<a href"):
                gsw_last_game_table += gsw_last_game_meta[i]
        i += 1
    i = 0
    while i < len(gsw_last_game_opponent_meta):
        if i < 1 or i > 3:
            if "over_header" in gsw_last_game_opponent_meta[i]:
                i += 8
                continue
            if not gsw_last_game_opponent_meta[i].strip().startswith("<a href"):
                gsw_last_game_opponent_table += gsw_last_game_opponent_meta[i]
        i += 1
    gsw_last_game_table = "<table style=\"margin: 0px auto;\" " + gsw_last_game_table.split("<table ")[1]
    gsw_last_game_opponent_table = "<table style=\"margin: 0px auto;\" " + gsw_last_game_opponent_table.split("<table ")[1]

# source5 = requests.get("https://www.cbssports.com/nba/teams/GS/golden-state-warriors/injuries/").text
# soup5 = BeautifulSoup(source5, 'lxml')
# gsw_injuries_meta = str(soup5.find("div", class_="Page-colMain").prettify()).split("\n")
# gsw_injuries = ""
# i = 0 
# while i < len(gsw_injuries_meta):
#     if "short" in gsw_injuries_meta[i]:
#         i += 6
#     elif "href" in gsw_injuries_meta[i]:
#         gsw_injuries += gsw_injuries_meta[i+1]
#         i += 3
#     elif "Updated" in gsw_injuries_meta[i]:
#         i += 1
#     elif "CellGameDate" in gsw_injuries_meta[i]:
#         gsw_injuries += gsw_injuries_meta[i]
#         i += 2
#     else:
#         gsw_injuries += gsw_injuries_meta[i]
#         i += 1

source5 = requests.get("https://www.basketball-reference.com/friv/injuries.fcgi").text
soup5 = BeautifulSoup(source5, 'lxml')
injuries_meta = soup5.find_all("tr")
for i in range(len(injuries_meta)):
    injuries_meta[i] = injuries_meta[i].prettify()
gsw_injuries = ""
for i in range(len(injuries_meta)):
    if "Warriors" in str(injuries_meta[i]):
        gsw_injuries += str(injuries_meta[i])
gsw_injuries_list = gsw_injuries.split("\n")
gsw_injuries = ""
i = 0
while i < len(gsw_injuries_list):
    if "team_name" in gsw_injuries_list[i]:
        i += 5
    elif gsw_injuries_list[i].strip().startswith("<a href"):
        gsw_injuries += gsw_injuries_list[i+1]
        i += 3
    else: 
        gsw_injuries += gsw_injuries_list[i]
        i += 1
gsw_injuries_table = ""
if gsw_injuries != "":
    gsw_injuries_table = "<div class=\"injuries_table\"><table style=\"margin: 0px auto;\" ><colgroup><col><col><col></colgroup><thead><tr><th>Player</th><th>Update</th><th>Description</th></tr></thead><tbody>" + gsw_injuries + "</tbody></table></div>"

source6 = requests.get("https://www.basketball-reference.com/teams/GSW/2023.html").text
soup6 = BeautifulSoup(source6, 'lxml')
gsw_player_statistics_meta = str(soup6.find(id="per_game").prettify()).split("\n")
gsw_player_statistics = ""
i = 0
while i < len(gsw_player_statistics_meta):
    if "caption" in gsw_player_statistics_meta[i]:
        i += 3
    if gsw_player_statistics_meta[i].strip().startswith("<a href"):
        gsw_player_statistics += gsw_player_statistics_meta[i+1]
        i += 3
    else:
        gsw_player_statistics += gsw_player_statistics_meta[i]
        i += 1
gsw_player_statistics = "<div class=\"player-stats\"><table style=\"margin: 0px auto;\" " + gsw_player_statistics.split("<table ")[1] + "</div>"

app = Flask(__name__)

@app.route("/standings")
def standings():
    return {
        "standing": gsw_standing,
        "wl": gsw_wl,
        "rankings": gsw_rankings,
        "ranking_numbers": gsw_ranking_numbers,
        "ranking_titles": gsw_ranking_titles,
        "ranking_units": gsw_ranking_units,
    }

@app.route("/recent")
def recent():
    return {
        "last_game": gsw_last_game,
        "next_game": gsw_next_game
    }

@app.route("/last-game")
def last_game():
    return {
        "last_game": gsw_last_game_table,
        "last_game_opponent": gsw_last_game_opponent_table
    }

@app.route("/injuries")
def injuries():
    return {
        "injuries": gsw_injuries_table
    }

@app.route("/player-stats")
def player_stats():
    return {
        "player_stats": gsw_player_statistics
    }

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5001)
