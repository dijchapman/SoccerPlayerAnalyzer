import pandas as pd
import requests
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec
from pandas.io import json

import playerplots


def matchWebscraper(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    scripts = soup.find_all('script')
    shots_data = scripts[1].string
    ind_start = shots_data.index("('")+2
    ind_end = shots_data.index("')")

    json_data = shots_data[ind_start:ind_end]
    json_data = json_data.encode('utf8').decode('unicode_escape')

    data = json.loads(json_data)
    return data


def playerWebscraper(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')

    page_title = soup.find_all('title')[0].string
    ind_end = page_title.index(" |")
    player_name = page_title[:ind_end]

    scripts = soup.find_all('script')
    shots_data = scripts[3].string
    ind_start = shots_data.index("('")+2
    ind_end = shots_data.index("')")

    json_data = shots_data[ind_start:ind_end]
    json_data = json_data.encode('utf8').decode('unicode_escape')

    data = json.loads(json_data)
    return data, player_name


def playerDataFrame(data):
    x = []
    y = []
    xG = []
    result = []
    situation = []
    season = []
    shot_type = []
    goals = []

    for index in range(len(data)):
        for key in data[index]:
            if key == 'X':
                x.append(float(data[index][key]))
            if key == 'Y':
                y.append(float(data[index][key]))
            if key == 'xG':
                xG.append(float(data[index][key]))
            if key == 'result':
                result.append(data[index][key])
                if data[index][key] == 'Goal':
                    goals.append(float(1))
                else:
                    goals.append(float(0))
            if key == 'situation':
                situation.append(data[index][key])
            if key == 'season':
                season.append(data[index][key])
            if key == 'shotType':
                shot_type.append(data[index][key])

    col_names = ['x', 'y', 'xG', 'result', 'situation', 'season', 'shotType', 'Goals']
    df = pd.DataFrame([x, y, xG, result, situation, season, shot_type, goals], index=col_names)
    df = df.T

    return df


def matchDataFrame(data):
    x = []
    y = []
    xG = []
    result = []
    team = []
    data_away = data['a']
    data_home = data['h']

    for index in range(len(data_home)):
        for key in data_home[index]:
            if key == 'X':
                x.append(data_home[index][key])
            if key == 'Y':
                y.append(data_home[index][key])
            if key == 'h_team':
                team.append(data_home[index][key])
            if key == 'xG':
                xG.append(data_home[index][key])
            if key == 'result':
                result.append(data_home[index][key])

    for index in range(len(data_away)):
        for key in data_away[index]:
            if key == 'X':
                x.append(data_away[index][key])
            if key == 'Y':
                y.append(data_away[index][key])
            if key == 'a_team':
                team.append(data_away[index][key])
            if key == 'xG':
                xG.append(data_away[index][key])
            if key == 'result':
                result.append(data_away[index][key])

    col_names = ['x', 'y', 'xG', 'result', 'team']
    df = pd.DataFrame([x, y, xG, result, team], index=col_names)
    df = df.T

    return df


def getMatchData(match_id):
    url = "https://understat.com/match/" + str(match_id)
    data = matchWebscraper(url)
    df = matchDataFrame(data)
    print(df)


def getPlayerData(player_id):
    url = "https://understat.com/player/" + str(player_id)
    data, player_name = playerWebscraper(url)
    df = playerDataFrame(data)
    df = df[df['season'] == '2021']
    return df, player_name


def showPlayerPlots(player_df, player_name, fig, gs):
    ax_shotmap = playerplots.showShotMap(player_df, fig, gs, 0, 0)
    ax_shotmap.title.set_text('Shot Map')

    player_columns = ['Goals', 'xG']
    n_rolling = 10
    ax_xGCum = playerplots.goalsToExpGoalsCumSumPlot(player_df, player_columns, fig, gs, 1, 0)
    ax_xGRolling = playerplots.goalsToExpGoalsRollingPlot(player_df, player_columns, fig, gs, 1, 1, n_rolling)
    ax_xGCum.title.set_text('Cumulative Goals vs xG')
    ax_xGRolling.title.set_text(str(n_rolling) + '-shot Rolling Goals vs xG')

    return ax_shotmap, ax_xGCum, ax_xGRolling


def main():
    player_df, player_name = getPlayerData("2371")

    fig = plt.figure(figsize=(10, 10))
    fig.suptitle('Player Analysis: ' + str(player_name), fontsize=16)
    gs = GridSpec(nrows=2, ncols=2, height_ratios=[2, 1])
    ax_shotmap, ax_xGCum, ax_xGRolling = showPlayerPlots(player_df, player_name, fig, gs)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # calling main function
    main()
