import pandas as pd
import requests
from bs4 import BeautifulSoup, Comment
from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec
import codecs

import playerplots
import understatscraper


def getWebPage(url):
    # Downloading contents of the web page
    data = requests.get(url).text

    # Creating BeautifulSoup object
    soup = BeautifulSoup(data, 'html.parser')
    return soup


def playersDataFrameStandard():
    url = "https://fbref.com/en/comps/9/stats/Premier-League-Stats"
    soup = getWebPage(url)

    # pc = BeautifulSoup(soup.content.decode('utf-8'), "html.parser")

    names = []
    positions = []
    teams = []
    year_born = []
    minutes = []
    ninty_minutes = []
    goals = []
    assists = []
    xg = []
    xa = []
    npxg = []
    for item in soup.find_all(text=lambda text: isinstance(text, Comment)):
        data = BeautifulSoup(item, "html.parser")
        if not data.find('table', id='stats_shooting') == 'None':
            for row in data.find_all('tr'):
                columns_td = row.find_all('td')
                if len(columns_td) > 0:
                    player_name_string = columns_td[0].string
                    # player_name_decode = pc.decode('utf-8')
                    # player_name = player_name_decode.lower()
                    # names.append(player_name)
                    positions.append(columns_td[2].string)
                    teams.append(columns_td[3].string)
                    year_born.append(columns_td[5].string)
                    minutes.append(float(columns_td[8].string.replace(",", "")))
                    ninty_minutes.append(float(columns_td[9].string))
                    goals.append(float(columns_td[17].string))
                    assists.append(float(columns_td[18].string))
                    xg.append(float(columns_td[26].string))
                    xa.append(float(columns_td[27].string))
                    npxg.append(float(columns_td[29].string))

    players_data = {
        'Player Name': names,
        'Position': positions,
        'Team': teams,
        'Year Born': year_born,
        'Minutes': minutes,
        'Ninty Minutes': ninty_minutes,
        'Goals': goals,
        'Assists': assists,
        'xG': xg,
        'npxG': npxg,
        'xA': xa
    }

    players_df = pd.DataFrame(players_data)
    return players_df


def playersDataFrameShooting():
    url = "https://fbref.com/en/comps/9/shooting/Premier-League-Stats"
    soup = getWebPage(url)

    sot_perc = []
    shots_p90 = []
    shotsOT_p90 = []
    for item in soup.find_all(text=lambda text: isinstance(text, Comment)):
        data = BeautifulSoup(item, "html.parser")
        if not data.find('table', id='stats_shooting') == 'None':
            for row in data.find_all('tr'):
                columns_td = row.find_all('td')
                if len(columns_td) > 0:
                    sot_perc.append(columns_td[10].string)
                    shots_p90.append(float(columns_td[11].string))
                    shotsOT_p90.append(float(columns_td[12].string))

    players_data = {
        'SoT Percentage': sot_perc,
        'Shots': shots_p90,
        'Shots On Target': shotsOT_p90
    }

    players_df = pd.DataFrame(players_data)
    return players_df


def playersDataFramePassing():
    url = "https://fbref.com/en/comps/9/passing/Premier-League-Stats"
    soup = getWebPage(url)

    key_passes = []
    final_third_passes = []
    progressive_passes = []
    for item in soup.find_all(text=lambda text: isinstance(text, Comment)):
        data = BeautifulSoup(item, "html.parser")
        if not data.find('table', id='stats_shooting') == 'None':
            for row in data.find_all('tr'):
                columns_td = row.find_all('td')
                if len(columns_td) > 0:
                    key_passes.append(float(columns_td[24].string))
                    final_third_passes.append(float(columns_td[25].string))
                    progressive_passes.append(float(columns_td[28].string))

    players_data = {
        'Key Passes': key_passes,
        'Final Third Passes': final_third_passes,
        'Progressive Passes': progressive_passes
    }

    players_df = pd.DataFrame(players_data)
    return players_df


def playersDataFrameDefending():
    url = "https://fbref.com/en/comps/9/defense/Premier-League-Stats"
    soup = getWebPage(url)

    tackles = []
    tackles_won = []
    dribbled_past = []
    pressures = []
    pressures_success = []
    blocks = []
    interceptions = []
    clearances = []
    for item in soup.find_all(text=lambda text: isinstance(text, Comment)):
        data = BeautifulSoup(item, "html.parser")
        if not data.find('table', id='stats_shooting') == 'None':
            for row in data.find_all('tr'):
                columns_td = row.find_all('td')
                if len(columns_td) > 0:
                    tackles.append(float(columns_td[7].string))
                    tackles_won.append(float(columns_td[8].string))
                    dribbled_past.append(float(columns_td[15].string))
                    pressures.append(float(columns_td[16].string))
                    pressures_success.append(float(columns_td[17].string))
                    blocks.append(float(columns_td[22].string))
                    interceptions.append(float(columns_td[26].string))
                    clearances.append(float(columns_td[28].string))

    players_data = {
        'Tackles': tackles,
        'Tackles Won': tackles_won,
        'Dribbled Past': dribbled_past,
        'Pressures': pressures,
        'Pressures Success': pressures_success,
        'Blocks': blocks,
        'Interceptions': interceptions,
        'Clearances': clearances
    }

    players_df = pd.DataFrame(players_data)
    return players_df


def playersDataFramePossession():
    url = "https://fbref.com/en/comps/9/possession/Premier-League-Stats"
    soup = getWebPage(url)

    touches_penalty_area = []
    dribbles_success = []
    dribbles_attempted = []
    carries_progressive = []
    carries_final_third = []
    dispossessed = []
    receiving_progressions = []
    for item in soup.find_all(text=lambda text: isinstance(text, Comment)):
        data = BeautifulSoup(item, "html.parser")
        if not data.find('table', id='stats_shooting') == 'None':
            for row in data.find_all('tr'):
                columns_td = row.find_all('td')
                if len(columns_td) > 0:
                    touches_penalty_area.append(float(columns_td[12].string))
                    dribbles_success.append(float(columns_td[14].string))
                    dribbles_attempted.append(float(columns_td[15].string))
                    carries_progressive.append(float(columns_td[22].string))
                    carries_final_third.append(float(columns_td[23].string))
                    dispossessed.append(float(columns_td[26].string))
                    receiving_progressions.append(float(columns_td[30].string))

    players_data = {
        'Touches Penalty Area': touches_penalty_area,
        'Dribbles Success': dribbles_success,
        'Dribbles': dribbles_attempted,
        'Carries Progressive': carries_progressive,
        'Carries Final Third': carries_final_third,
        'Dispossessed': dispossessed,
        'Receiving Progressive': receiving_progressions
    }

    players_df = pd.DataFrame(players_data)
    return players_df


def playersDataFrameMisc():
    url = "https://fbref.com/en/comps/9/misc/Premier-League-Stats"
    soup = getWebPage(url)

    fouls_committed = []
    fouls_drawn = []
    recoveries = []
    aerial_duels_won = []
    aerial_duels_lost = []
    aerial_duels_won_perc = []
    for item in soup.find_all(text=lambda text: isinstance(text, Comment)):
        data = BeautifulSoup(item, "html.parser")
        if not data.find('table', id='stats_shooting') == 'None':
            for row in data.find_all('tr'):
                columns_td = row.find_all('td')
                if len(columns_td) > 0:
                    fouls_committed.append(float(columns_td[10].string))
                    fouls_drawn.append(float(columns_td[11].string))
                    recoveries.append(float(columns_td[19].string))
                    aerial_duels_won.append(float(columns_td[20].string))
                    aerial_duels_lost.append(float(columns_td[21].string))
                    aerial_duels_won_perc.append(columns_td[22].string)

    players_data = {
        'Fouls Committed': fouls_committed,
        'Fouls Drawn': fouls_drawn,
        'Recoveries': recoveries,
        'Aerial Duels Won': aerial_duels_won,
        'Aerial Duels Lost': aerial_duels_lost,
        'Aerial Duels Won Percent': aerial_duels_won_perc
    }

    players_df = pd.DataFrame(players_data)
    return players_df


def updateStatsPer90(players_df):
    metrics_to_update = [
        'Shots',
        'Shots On Target',
        'Key Passes',
        'Final Third Passes',
        'Progressive Passes',
        'Tackles',
        'Tackles Won',
        'Dribbled Past',
        'Pressures',
        'Pressures Success',
        'Blocks',
        'Interceptions',
        'Clearances',
        'Touches Penalty Area',
        'Dribbles Success',
        'Dribbles',
        'Carries Progressive',
        'Carries Final Third',
        'Dispossessed',
        'Receiving Progressive',
        'Fouls Committed',
        'Fouls Drawn',
        'Recoveries',
        'Aerial Duels Won',
        'Aerial Duels Lost'
    ]
    for metric in metrics_to_update:
        players_df[metric] = players_df[metric] / players_df['Ninty Minutes']

    players_df['Aerial Duels Total'] = players_df['Aerial Duels Won'] + players_df['Aerial Duels Lost']

    return players_df


def getPlayerData():
    players_df_standard = playersDataFrameStandard()
    players_df_shooting = playersDataFrameShooting()
    players_df_passing = playersDataFramePassing()
    players_df_defending = playersDataFrameDefending()
    players_df_possession = playersDataFramePossession()
    players_df_misc = playersDataFrameMisc()
    players_df = pd.concat([players_df_standard, players_df_shooting, players_df_passing, players_df_defending, players_df_possession, players_df_misc], axis=1, join="inner")

    players_df = updateStatsPer90(players_df)
    players_df.set_index('Player Name', inplace=True)
    return players_df


def showPlayerCard(understat_id, position):
    shots_df, pn = understatscraper.getPlayerData(understat_id)
    players_df = loadFromCSV()
    players_df = players_df[players_df['Position'].str.contains(position)]

    player_name = pn.lower()

    fig = plt.figure(figsize=(12, 8))
    player_age = players_df.loc[player_name, 'Year Born']
    player_team = players_df.loc[player_name, 'Team']
    fig.suptitle('Player Analysis: ' + pn + ' (' + str(player_age) + ', ' + player_team + ')', fontsize=16)
    gs = GridSpec(nrows=2, ncols=2)

    metrics_list = [
                   'xG',
                   'Goals',
                   'Shots',
                   'xA',
                   'Key Passes',
                   'Final Third Passes',
                   'Progressive Passes',
                   'Receiving Progressive',
                   'Carries Progressive',
                   'Dribbles Success',
                   'Interceptions',
                   'Pressures Success',
                   'Recoveries',
                   'Aerial Duels Won',
                   'Aerial Duels Won Percent'
               ]

    metrics_colors = [3, 3, 3, 2, 5]

    ax_polar = playerplots.showPolarGraph(players_df, player_name, player_team, metrics_list,
                                          metrics_colors, fig, gs, 0, 0, 1, 1)
    ax_shotmap, ax_xGCum, ax_xGRolling = understatscraper.showPlayerPlots(shots_df, player_name, fig, gs)
    plt.show()


def loadFromCSV():
    players_df = pd.read_csv('fbref_data.csv')
    players_df.set_index('Player Name', inplace=True)
    return players_df


def saveToCSV():
    players_df = getPlayerData()
    players_df.to_csv('fbref_data.csv')


def main():
    saveToCSV()
    find_player = '618'
    while find_player != "exit":
        find_player = input("Enter understat ID: ")
        if find_player != "exit":
            position = input("Enter position (GK, DF, MF, FW): ")
            showPlayerCard(find_player, position)

    print("Closing analyser...")


if __name__ == "__main__":
    # calling main function
    main()
