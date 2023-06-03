import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np
import pandas as pd

import playerplots
import wyscoutmetrics


def showScatterGraph(players_df, x_axis_stat, y_axis_stat, maximum_age, lines="quadrants"):
    x_stats = np.array(players_df[x_axis_stat])
    x_50 = np.percentile(x_stats, 50)
    x_min = min(players_df[x_axis_stat])
    x_max = max(players_df[x_axis_stat])

    y_stats = np.array(players_df[y_axis_stat])
    y_50 = np.percentile(y_stats, 50)
    y_min = min(players_df[y_axis_stat])
    y_max = max(players_df[y_axis_stat])

    # give some space with the min and max values
    padding = 0.1
    x_min = x_min * (1 - padding)
    x_max = x_max * (1 + padding)
    y_min = y_min * (1 - padding)
    y_max = y_max * (1 + padding)

    filteredPlayers = players_df.loc[players_df['Age'] <= int(maximum_age)]

    # Scatter plot
    ax = filteredPlayers.plot.scatter(x=x_axis_stat, y=y_axis_stat, alpha=0.5)

    # Annotate each data point
    for i, txt in enumerate(filteredPlayers.index):
        ax.annotate(txt, (filteredPlayers[x_axis_stat].iat[i] + ((x_max - x_min) / 50),
                          filteredPlayers[y_axis_stat].iat[i]))

    if lines == 'best_fit':
        # find line of best fit
        a, b = np.polyfit(x_stats, y_stats, 1)

        x_stats_sorted = np.sort(x_stats)
        x_line_best_fit = [
            x_stats_sorted[0],
            x_stats_sorted[len(x_stats_sorted) - 1]
        ]
        y_line_best_fit = [
            a * x_stats_sorted[0] + b,
            a * x_stats_sorted[len(x_stats_sorted) - 1] + b
        ]

        if y_stats.max() > y_line_best_fit[1]:
            y_line_best_fit[1] = (y_stats.max() - b) / a

        # x_line_best_fit = [x_min, x_max]
        # y_line_best_fit = [y_min, y_max]

        x_line_top_players = [x_min, (x_max * 0.75)]
        x_line_bottom_players = [x_min, (x_max * 1.25)]

        plt.plot(x_line_best_fit, y_line_best_fit, color='black', linestyle='--', linewidth=1)
        plt.plot(x_line_top_players, y_line_best_fit, color='black', linestyle='--', linewidth=1)
        plt.plot(x_line_bottom_players, y_line_best_fit, color='black', linestyle='--', linewidth=1)
        ax.fill_between(x_line_best_fit, y_line_best_fit, max(y_line_best_fit), interpolate=True, color='springgreen',
                        alpha=0.2)
        ax.fill_between(x_line_top_players, y_line_best_fit, max(y_line_best_fit), interpolate=True, color='limegreen',
                        alpha=0.2)
        ax.fill_between(x_line_best_fit, 0, y_line_best_fit, interpolate=True, color='indianred', alpha=0.2)
        ax.fill_between(x_line_bottom_players, 0, y_line_best_fit, interpolate=True, color='firebrick', alpha=0.2)
    elif lines == 'quadrants':
        plt.plot([x_50, x_50], [y_min, y_max], color='black', linestyle='--', linewidth=1)
        plt.plot([x_min, x_max], [y_50, y_50], color='black', linestyle='--', linewidth=1)
        ax.fill_between([x_50, x_max], y_50, y_max, interpolate=True, color='limegreen', alpha=0.3)  # top right box
        ax.fill_between([x_50, x_max], y_min, y_50, interpolate=True, color='gold', alpha=0.3)  # bottom right box
        ax.fill_between([x_min, x_50], y_50, y_max, interpolate=True, color='gold', alpha=0.3)  # top left box
        ax.fill_between([x_min, x_50], y_min, y_50, interpolate=True, color='indianred', alpha=0.3)  # bottom left box

    ax.scatter(x_stats, y_stats, s=20, color="blue")
    plt.xlim([x_min, x_max])
    plt.ylim([y_min, y_max])
    plt.grid(linestyle='--', linewidth=0.5, alpha=0.7)
    plt.show()


def showPlayerBarGraph(players_df, player_name, fig, gs):
    ax = fig.add_subplot(gs[:2, :2])
    stat_names = []
    player_stats_percentile = []
    colors = []
    for statName in players_df.iloc[:, 2:]:
        stat_names.append(statName)
        players_df['Percentile Rank'] = players_df[statName].rank(pct=True)
        percentile_score = players_df.loc[player_name]['Percentile Rank'] * 100
        player_stats_percentile.append(percentile_score)
        colors.append('slateblue')

    ax.title.set_text('Bar Graph')
    ax.set_xlim([0, 100])
    ax.barh(np.array(stat_names), np.array(player_stats_percentile), color=colors, alpha=0.6)
    ax.set_xticklabels([])
    for tick in ax.yaxis.get_majorticklabels():
        tick.set_horizontalalignment("left")
    ax.tick_params(axis="y", direction="in", pad=-15)
    return ax


def showSinglePlayerScatterGraph(players_df, x_axis_stat, y_axis_stat, player_name, fig, gs, subplot_row, subplot_col):
    x_stats = np.array(players_df[x_axis_stat])
    y_stats = np.array(players_df[y_axis_stat])

    highlighted_player = players_df.loc[player_name]

    ax = fig.add_subplot(gs[subplot_row, subplot_col])
    ax.scatter(x=x_stats, y=y_stats, alpha=0.3, s=15, color="blue")
    ax.scatter(x=highlighted_player[x_axis_stat], y=highlighted_player[y_axis_stat], s=40, color="green")

    return ax


def showPlayerCard(players_df, player_name, position, position_type1, position_type2):
    # find best position type
    position_type = position_type1
    if players_df.loc[player_name, position_type2 + '_Score_100'] > \
            players_df.loc[player_name, position_type1 + '_Score_100']:
        position_type = position_type2

    similar_players, similar_players_teams = findSimilarPlayers(players_df, player_name, position_type)

    player_team = players_df.loc[player_name, 'Team']
    player_info = "(Age: " + str(players_df.loc[player_name, 'Age']) + \
                  "; Positions: " + str(players_df.loc[player_name, 'Position']) + \
                  "; Foot: " + str(players_df.loc[player_name, 'Foot']) + \
                  "; Team: " + player_team + ')'

    fig = plt.figure(figsize=(12, 8))
    fig.suptitle('Player Analysis: ' + player_name + '\n' + player_info, fontsize=14)
    gs = GridSpec(nrows=3, ncols=4, height_ratios=[2, 2, 2], width_ratios=[1, 1, 1, 1])

    metrics_list, metrics_colors = wyscoutmetrics.getPolarChartPositionMetrics(position)
    scatter_metrics = wyscoutmetrics.getScatterPlotMetrics(position)

    ax_polar = playerplots.showMetricsRadar(players_df, player_name, player_team, metrics_list,
                                            metrics_colors, fig, gs, 0, 2, 0, 2, True)

    metrics_list = [
        'Forward Passes %',
        'Lateral Passes %',
        'Back Passes %',
        'Back passes per 90',
        'Lateral passes per 90',
        'Forward passes per 90'
    ]
    passing_radar = playerplots.showPassingRadar(players_df, player_name, player_team, metrics_list, fig, gs, 0, 0, 2,
                                                 2)
    passing_radar.title.set_text('Passing Direction')

    attributes_list = wyscoutmetrics.attributeMetricsWeights(position_type1).keys()
    metrics_colors = [1, 3, 2, 2]

    attributes_list = wyscoutmetrics.attributeMetricsWeights(position_type2).keys()
    ax_attributes_type = playerplots.showAttributeRadar(players_df, player_name, player_team, attributes_list,
                                                        metrics_colors, fig, gs, 1, 1, 2, 2, True,
                                                        rating_label=position_type + '_Score_100')

    # player_game_df = pd.read_csv('Player stats.csv')
    # player_columns = ['Goals', 'xG']
    # n_rolling = 7
    # ax_xGCum = playerplots.goalsToExpGoalsCumSumPlot(player_game_df, player_columns, fig, gs, 0, 3)
    # ax_xGRolling = playerplots.goalsToExpGoalsRollingPlot(player_game_df, player_columns, fig, gs, 1, 3, n_rolling)
    # ax_xGCum.title.set_text('Cumulative Goals vs xG')
    # ax_xGRolling.title.set_text(str(n_rolling) + '-game Rolling Goals vs xG')

    ax_polar_similar1 = playerplots.showAttributeRadar(players_df, similar_players[0], similar_players_teams[0],
                                                       attributes_list, metrics_colors, fig, gs, 0, 0, 3, 3, False)
    ax_polar_similar1.title.set_text('Similar Player:\n' + str(similar_players[0]) + ', ' + similar_players_teams[0])
    ax_polar_similar1.title.set_fontsize(10)

    ax_polar_similar2 = playerplots.showAttributeRadar(players_df, similar_players[1], similar_players_teams[1],
                                                       attributes_list, metrics_colors, fig, gs, 1, 1, 3, 3, False)
    ax_polar_similar2.title.set_text('Similar Player:\n' + str(similar_players[1]) + ', ' + similar_players_teams[1])
    ax_polar_similar2.title.set_fontsize(10)

    ax_scatter1 = showSinglePlayerScatterGraph(players_df, scatter_metrics[0][1], scatter_metrics[0][2],
                                               player_name, fig, gs, 2, 0)
    ax_scatter1.title.set_text(scatter_metrics[0][0])
    ax_scatter1.title.set_fontsize(10)

    ax_scatter2 = showSinglePlayerScatterGraph(players_df, scatter_metrics[1][1], scatter_metrics[1][2],
                                               player_name, fig, gs, 2, 1)
    ax_scatter2.title.set_text(scatter_metrics[1][0])
    ax_scatter2.title.set_fontsize(10)

    ax_scatter3 = showSinglePlayerScatterGraph(players_df, scatter_metrics[2][1], scatter_metrics[2][2],
                                               player_name, fig, gs, 2, 2)
    ax_scatter3.title.set_text(scatter_metrics[2][0])
    ax_scatter3.title.set_fontsize(10)

    ax_scatter4 = showSinglePlayerScatterGraph(players_df, scatter_metrics[3][1], scatter_metrics[3][2],
                                               player_name, fig, gs, 2, 3)
    ax_scatter4.title.set_text(scatter_metrics[3][0])
    ax_scatter4.title.set_fontsize(10)

    plt.subplots_adjust(bottom=0.1, left=0.1, top=0.8, right=0.8)
    plt.tight_layout()
    plt.show()


def findSimilarPlayers(players_df, player_name, position):
    players_df['SimilarityScore'] = 0

    for index, player in players_df.iterrows():
        similarity_score = 0
        for attribute in wyscoutmetrics.attributeMetricsWeights(position).keys():
            metric_high = players_df[attribute].max()
            metric_low = players_df[attribute].min()
            sim_score = ((player[attribute] - players_df.loc[player_name, attribute]) / (
                    metric_high - metric_low)) * 100
            similarity_metric_score = sim_score ** 2
            similarity_score += similarity_metric_score
        players_df.at[index, 'SimilarityScore'] = similarity_score

    player_team = players_df.loc[player_name, 'Team']

    # remove player searching for from DataFrame
    players_df = players_df.drop(player_name)

    # remove players from the same club
    players_df.drop(players_df[players_df['Team'] == player_team].index, inplace=True)

    similar_players_df = players_df.sort_values(by=['SimilarityScore'])
    similar_players_df = similar_players_df[:2]
    similar_players = list(similar_players_df.index.values)
    similar_players_teams = list(similar_players_df['Team'])
    return similar_players, similar_players_teams


def calculateNewMetrics(players_df):
    players_df['Short / Medium Passes %'] = players_df['Short / medium passes per 90'] / players_df[
        'Passes per 90'] * 100
    players_df['Long Passes %'] = players_df['Long passes per 90'] / players_df['Passes per 90'] * 100
    players_df['Forward Passes %'] = players_df['Forward passes per 90'] / players_df['Passes per 90'] * 100
    players_df['Lateral Passes %'] = players_df['Lateral passes per 90'] / players_df['Passes per 90'] * 100
    players_df['Back Passes %'] = players_df['Back passes per 90'] / players_df['Passes per 90'] * 100
    players_df['Progressive Passes %'] = players_df['Progressive passes per 90'] / players_df['Passes per 90'] * 100
    players_df['Accurate Passes per 90'] = players_df['Passes per 90'] * players_df['Accurate passes, %'] / 100
    players_df['Accurate Long Passes per 90'] = players_df['Long passes per 90'] * players_df['Accurate long passes, %'] / 100
    players_df['Accurate Forward Passes per 90'] = players_df['Forward passes per 90'] * players_df[
        'Accurate forward passes, %'] / 100
    players_df['Accurate Passes to final third per 90'] = players_df['Passes to final third per 90'] * players_df[
        'Accurate passes to final third, %'] / 100
    players_df['Accurate Progressive Passes per 90'] = players_df['Progressive passes per 90'] * players_df[
        'Accurate progressive passes, %'] / 100
    players_df['Accurate Forward Passes per 90'] = players_df['Forward passes per 90'] * players_df[
        'Accurate forward passes, %'] / 100

    teams_df = pd.read_csv('Team Stats.csv')
    teams_df.set_index('Team', inplace=True)
    for index, player in players_df.iterrows():
        if player['Team'] in teams_df.index:
            players_df.at[index, '% of Team Goals'] = player['Goals per 90'] / teams_df.loc[
                player['Team'], 'Total Goals'] * 100
            players_df.at[index, '% of Team xG'] = player['xG per 90'] / teams_df.loc[player['Team'], 'Total xG'] * 100
            players_df.at[index, '% of Team Assists'] = player['Assists per 90'] / teams_df.loc[
                player['Team'], 'Total Goals'] * 100
            players_df.at[index, '% of Team xA'] = player['xA per 90'] / teams_df.loc[player['Team'], 'Total xG'] * 100
            players_df.at[index, '% of Team Shots'] = player['Shots per 90'] / teams_df.loc[
                player['Team'], 'Shots'] * 100
            players_df.at[index, '% of Team Shots Assists'] = player['Shot assists per 90'] / teams_df.loc[
                player['Team'], 'Shots'] * 100
            players_df.at[index, '% of Team Crosses'] = player['Crosses per 90'] / teams_df.loc[
                player['Team'], 'Crosses'] * 100
            players_df.at[index, '% of Team Dribbles'] = player['Dribbles per 90'] / teams_df.loc[
                player['Team'], 'Dribbles'] * 100
            players_df.at[index, '% of Team Touches in box'] = player['Touches in box per 90'] / teams_df.loc[
                player['Team'], 'Touches in penalty area'] * 100
            players_df.at[index, '% of Team Defensive duels'] = player['Defensive duels per 90'] / teams_df.loc[
                player['Team'], 'Defensive duels'] * 100
            players_df.at[index, '% of Team Interceptions'] = player['PAdj Interceptions'] / teams_df.loc[
                player['Team'], 'Interceptions'] * 100
            players_df.at[index, '% of Team Passes'] = player['Passes per 90'] / teams_df.loc[
                player['Team'], 'Passes'] * 100
            players_df.at[index, '% of Team Through passes'] = player['Through passes per 90'] / teams_df.loc[
                player['Team'], 'Through passes'] * 100
            players_df.at[index, '% of Team Key passes'] = player['Key passes per 90'] / teams_df.loc[
                player['Team'], 'Key passes'] * 100
            players_df.at[index, '% of Team To final third passes'] = \
                player['Passes to final third per 90'] / teams_df.loc[player['Team'], 'To final third'] * 100
            players_df.at[index, '% of Team Progressive passes'] = player['Progressive passes per 90'] / teams_df.loc[
                player['Team'], 'Progressive passes'] * 100
            players_df.at[index, '% of Team Progressive runs'] = player['Progressive runs per 90'] / teams_df.loc[
                player['Team'], 'Progressive runs'] * 100
            players_df.at[index, '% of Team Deep completions'] = player['Deep completions per 90'] / teams_df.loc[
                player['Team'], 'Deep completions'] * 100

    players_df['% of Team Goals'] = players_df['% of Team Goals'].fillna(0)
    players_df['% of Team xG'] = players_df['% of Team xG'].fillna(0)
    players_df['% of Team xA'] = players_df['% of Team xA'].fillna(0)
    players_df['% of Team Shots'] = players_df['% of Team Shots'].fillna(0)
    players_df['% of Team Shots Assists'] = players_df['% of Team Shots Assists'].fillna(0)
    players_df['% of Team Crosses'] = players_df['% of Team Crosses'].fillna(0)
    players_df['% of Team Dribbles'] = players_df['% of Team Dribbles'].fillna(0)
    players_df['% of Team Touches in box'] = players_df['% of Team Touches in box'].fillna(0)
    players_df['% of Team Defensive duels'] = players_df['% of Team Defensive duels'].fillna(0)
    players_df['% of Team Interceptions'] = players_df['% of Team Interceptions'].fillna(0)
    players_df['% of Team Passes'] = players_df['% of Team Passes'].fillna(0)
    players_df['% of Team Through passes'] = players_df['% of Team Through passes'].fillna(0)
    players_df['% of Team Key passes'] = players_df['% of Team Key passes'].fillna(0)
    players_df['% of Team To final third passes'] = players_df['% of Team To final third passes'].fillna(0)
    players_df['% of Team Progressive passes'] = players_df['% of Team Progressive passes'].fillna(0)
    players_df['% of Team Progressive runs'] = players_df['% of Team Progressive runs'].fillna(0)
    players_df['% of Team Deep completions'] = players_df['% of Team Deep completions'].fillna(0)

    return players_df


def calculateAttributeScores(players_df, position):
    all_metrics = wyscoutmetrics.attributeMetrics('all')

    for metric in all_metrics:
        metric_zscore = metric + '_zscore'
        players_df[metric_zscore] = (players_df[metric] - players_df[metric].mean()) / players_df[metric].std(ddof=0)
        players_df[metric_zscore] = ((players_df[metric_zscore] - players_df[metric_zscore].min()) /
                                     (players_df[metric_zscore].max() - players_df[metric_zscore].min())) * 100

    for attr, weight in wyscoutmetrics.attributeMetricsWeights(position).items():
        metrics_list = wyscoutmetrics.attributeMetrics(attr)
        if not metrics_list == 'none':
            players_df[attr] = players_df[metrics_list].sum(axis=1)
            players_df[attr] = ((players_df[attr] - players_df[attr].min()) /
                                (players_df[attr].max() - players_df[attr].min())) * 100

    return players_df


def calculatePositionRating(players_df, position):
    attribute_weighting = wyscoutmetrics.attributeMetricsWeights(position)

    players_df[position + '_Score'] = players_df['Minutes played_zscore'] * attribute_weighting['Minutes played_zscore']
    for attr, weight in attribute_weighting.items():
        players_df[position + '_Score'] += players_df[attr] * weight

    players_df[position + '_Ranking'] = players_df[position + '_Score'].rank(method='max', ascending=False)
    players_df[position + '_Score_100'] = (players_df[position + '_Score'] / players_df[
        position + '_Score'].max()) * 100

    return players_df


def filterByLeagueAndPosition(players_df):
    league = input("Enter League (L2, NL or NLNS): ").upper()
    position = input("Enter Position (CB, WB, CM, AM, ST): ").upper()
    players_df = players_df[(players_df['League'] == league) & (players_df['Main Position'] == position)]

    position_type1 = 'BW'
    position_type2 = 'BP'
    if position == 'CB' or position == 'WB' or position == 'CM':
        # position_type_input = input("Enter Position Type (BW - Ball Winning or BP - Ball Playing): ").upper()
        position_type1 = position + ' BW'
        position_type2 = position + ' BP'
    elif position == 'AM':
        # position_type_input = input("Enter Position Type (BC - Ball Carrying or C - Creative): ").upper()
        position_type1 = position + ' BC'
        position_type2 = position + ' C'
    elif position == 'ST':
        # position_type_input = input("Enter Position Type (TM - Target Man or A - Advanced): ").upper()
        position_type1 = position + ' TM'
        position_type2 = position + ' A'

    players_df = calculateAttributeScores(players_df, position_type1)
    players_df = calculateAttributeScores(players_df, position_type2)
    players_df = calculatePositionRating(players_df, position_type1)
    players_df = calculatePositionRating(players_df, position_type2)
    players_df['Overall Score'] = (players_df[position_type1 + '_Score_100'] + players_df[
        position_type2 + '_Score_100']) / 2
    players_df = players_df.sort_values(by=['Overall Score'], ascending=False)

    show_columns = [
        'Team',
        'Team Now',
        'On loan',
        'Position',
        'Age',
        'Foot',
        'Height',
        'Minutes played',
        'Contract expires',
        position_type1 + '_Score_100',
        position_type2 + '_Score_100',
        'Overall Score'
    ]
    print(players_df.iloc[:10][show_columns])

    return league, position, position_type1, position_type2, players_df


def loadFromCSV():
    players_df = pd.read_csv('Search results.csv')

    players_df.set_index('Player', inplace=True)
    players_df['Age'] = players_df['Age'].fillna(0)
    players_df['Age'] = players_df['Age'].astype('int')

    return players_df


def teamPlayerMinutesByAge(players_df):
    teams_df = pd.read_csv('Team Stats.csv')
    teams_df = teams_df[teams_df['League'] == 'NL']

    fig = plt.figure(figsize=(12, 8))
    fig.suptitle('Team Age Distribution', fontsize=14)
    gs = GridSpec(nrows=5, ncols=5)

    youngest_age = players_df.loc[players_df['League'] == 'NL', 'Age'].min()
    oldest_age = players_df.loc[players_df['League'] == 'NL', 'Age'].max()

    prime_age_range = [24, 28]
    prime_age_range_fill = [prime_age_range[0] - 0.5, prime_age_range[1] + 0.5]

    row_number = 0
    col_number = 0
    for index, team in teams_df.iterrows():
        team_name = team['Team']
        team_players_df = players_df[players_df['Team'] == team_name]
        minutes_by_age = []
        minutes_x_age = 0
        total_minutes = 0
        young_minutes = 0
        prime_minutes = 0
        old_minutes = 0
        for age in range(youngest_age, oldest_age + 1):
            age_minutes = team_players_df.loc[team_players_df['Age'] == age, 'Minutes played'].sum()
            total_minutes += age_minutes
            minutes_x_age += (age_minutes * age)
            minutes_by_age.append(age_minutes)
            if age < prime_age_range[0]:
                young_minutes += age_minutes
            if prime_age_range[0] <= age <= prime_age_range[1]:
                prime_minutes += age_minutes
            if prime_age_range[1] < age:
                old_minutes += age_minutes
        average_age = round(minutes_x_age / total_minutes, 1)
        ax = fig.add_subplot(gs[row_number, col_number])
        ax.bar(range(youngest_age, oldest_age + 1), minutes_by_age, color=team['Team Color'])
        ax.fill_between(prime_age_range_fill, max(minutes_by_age) * 1.2,
                        interpolate=True, color='limegreen', alpha=0.5)
        ax.set_facecolor('#a1a1a1')
        ax.title.set_text(team_name + '\n(Average age: ' + str(average_age) + ')')
        ax.title.set_fontsize(10)
        teams_df.loc[index, 'Young Minutes'] = young_minutes
        teams_df.loc[index, 'Prime Minutes'] = prime_minutes
        teams_df.loc[index, 'Old Minutes'] = old_minutes
        col_number += 1
        if col_number >= 5:
            col_number = 0
            row_number += 1

    plt.subplots_adjust(bottom=0.1, left=0.1, top=0.8, right=0.8)
    plt.tight_layout()
    plt.show()

    fig = plt.figure(figsize=(12, 8))
    fig.suptitle('Team Age Distribution', fontsize=14)
    gs = GridSpec(nrows=1, ncols=3)

    teams_df = teams_df.sort_values('Young Minutes')
    ax = fig.add_subplot(gs[0, 0])
    ax.barh(teams_df['Team'], teams_df['Young Minutes'], color=teams_df['Team Color'])
    ax.tick_params(axis='x', rotation=80)
    ax.set_facecolor('#a1a1a1')
    ax.title.set_text('Minutes Given to players younger than ' + str(prime_age_range[0]))
    ax.title.set_fontsize(10)

    teams_df = teams_df.sort_values('Prime Minutes')
    ax = fig.add_subplot(gs[0, 1])
    ax.barh(teams_df['Team'], teams_df['Prime Minutes'], color=teams_df['Team Color'])
    ax.tick_params(axis='x', rotation=80)
    ax.set_facecolor('#a1a1a1')
    ax.title.set_text('Minutes Given to players in their prime (age ' + str(prime_age_range[0]) + '-' +
                      str(prime_age_range[1]) + ')')
    ax.title.set_fontsize(10)

    teams_df = teams_df.sort_values('Old Minutes')
    ax = fig.add_subplot(gs[0, 2])
    ax.barh(teams_df['Team'], teams_df['Old Minutes'], color=teams_df['Team Color'])
    ax.tick_params(axis='x', rotation=80)
    ax.set_facecolor('#a1a1a1')
    ax.title.set_text('Minutes Given to players older than ' + str(prime_age_range[1]))
    ax.title.set_fontsize(10)

    plt.subplots_adjust(bottom=0.1, left=0.1, top=0.8, right=0.8)
    plt.tight_layout()
    plt.show()


def main():
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', 1000)

    plt.style.use('dark_background')
    all_players_df = loadFromCSV()
    # teamPlayerMinutesByAge(all_players_df)

    all_players_df = calculateNewMetrics(all_players_df)
    league, position, position_type1, position_type2, players_df = filterByLeagueAndPosition(all_players_df)

    find_player = "scatter"

    while find_player != "exit":
        find_player = input("Enter player name (enter 'exit' to exit): ")
        if find_player == "scatter":
            for metric in players_df.columns[6:]:
                print(metric)
            x_axis_stat = input("Enter first metric: ")
            y_axis_stat = input("Enter second metric: ")
            maximum_age = input("Maximum Age: ")
            showScatterGraph(players_df, x_axis_stat, y_axis_stat, maximum_age)
        elif find_player == "reload":
            league, position, position_type1, position_type2, players_df = filterByLeagueAndPosition(all_players_df)
        elif find_player != "scatter" and find_player != "exit":
            if find_player in players_df.index:
                print(players_df.loc[find_player, 'Team Now':'On loan'])
                showPlayerCard(players_df, find_player, position, position_type1, position_type2)
            else:
                print("Can't find player, please try again")

    print("Closing analyser...")


if __name__ == "__main__":
    # calling main function
    main()
