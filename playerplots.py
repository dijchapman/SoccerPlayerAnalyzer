import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'


def goalsToExpGoalsCumSumPlot(players_df, player_columns, fig, gs, row, column):
    players_df = players_df[player_columns]
    players_df['GoalsGraph'] = players_df['Goals'].cumsum()
    players_df['xGGraph'] = players_df['xG'].cumsum()
    return showGameByGameChart(players_df, fig, gs, row, column)


def goalsToExpGoalsRollingPlot(players_df, player_columns, fig, gs, row, column, n_rolling):
    players_df = players_df[player_columns]
    players_df['GoalsGraph'] = players_df['Goals'].rolling(n_rolling).mean()
    players_df['xGGraph'] = players_df['xG'].rolling(n_rolling).mean()
    return showGameByGameChart(players_df, fig, gs, row, column)


def showGameByGameChart(players_df, fig, gs, row, column):
    players_df = players_df.astype({'GoalsGraph': 'float', 'xGGraph': 'float'})

    players_df['GoalsMinusXG'] = players_df['GoalsGraph'] - players_df['xGGraph']

    games = len(players_df['GoalsGraph'])

    ax = fig.add_subplot(gs[row, column])
    ax.set_xlim([0, games])
    ax.plot(range(0, games), players_df['GoalsMinusXG'], label='Goals')
    plt.fill_between(range(0, games), players_df['GoalsMinusXG'], 0,
                     where=players_df['GoalsMinusXG'] >= 0, facecolor='green', interpolate=True,
                     alpha=0.4)
    plt.fill_between(range(0, games), players_df['GoalsMinusXG'], 0,
                     where=players_df['GoalsMinusXG'] <= 0, facecolor='red', interpolate=True,
                     alpha=0.4)
    # ax.legend()

    return ax


def showPolarGraph(players_df, player_name, player_team, metrics_list, metrics_colors, fig, gs,
                   row_start, row_end, col_start, col_end, show_axis=True, theta_offset=1.8,
                   label_angle_offset=12, rating_label='Overall Score'):
    N = len(metrics_list)
    theta = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
    width = 2 * np.pi / N
    colors_list = ["palevioletred", "mediumorchid", "rebeccapurple", "slateblue", "lightgreen"]

    colors = []
    color_num = 0
    for color in metrics_colors:
        add_colors = [colors_list[color_num]] * color
        colors = colors + add_colors
        color_num += 1

    values = []
    for metric in metrics_list:
        players_df['Percentile Rank'] = players_df[metric].rank(pct=True)
        percentile_score = players_df.loc[player_name]['Percentile Rank'] * 100
        if isinstance(percentile_score, pd.Series):
            player = players_df.loc[player_name]
            player = player.loc[player['Team'] == player_team]
            percentile_score = player.loc[player_name]['Percentile Rank'] * 100
        values.append(percentile_score)

    if row_start == row_end:
        ax = fig.add_subplot(gs[row_start, col_start], projection='polar')
    else:
        ax = fig.add_subplot(gs[row_start:row_end, col_start:col_end], projection='polar')

    ax.bar(theta, values, width=width, bottom=0.0, color=colors, alpha=0.8, align='edge', edgecolor='white')
    ax.bar(theta, [100] * len(values), width=width, bottom=0.0, color=colors, alpha=0.4, align='edge')

    ax.set_yticklabels([])

    ax.set_theta_zero_location('N')
    ax.set_theta_offset(np.pi / theta_offset)
    ax.set_theta_direction(-1)
    ax.spines['polar'].set_color("grey")
    ax.spines['polar'].set_alpha(0.3)
    ax.tick_params(axis='x', which='major', pad=3)
    ax.grid(axis='y', color='grey', linestyle='--', alpha=0.5)

    bottom_hole = 25
    ax.set_rorigin(-bottom_hole)

    ax.set_thetagrids(range(0, 360, int(360 / len(metrics_list))), [])
    if show_axis:
        plt.text(-bottom_hole, -bottom_hole, str(round(players_df.loc[player_name, rating_label], 1)),
                 ha='center', va='center', fontsize=11)
        metric_num = 0
        for metric in metrics_list:
            vertical_align = 'bottom'
            label_angle = label_angle_offset + (metric_num * (360 / len(metrics_list)))
            text_rotation = 360 - (metric_num * (360 / len(metrics_list)))
            label_name = metric.replace(" per 90", "")
            label_name = label_name.replace("zscore", "")
            label_name = label_name.replace(" ", "\n")
            label_name = label_name.replace("_", "\n")
            if 270 > text_rotation > 90:
                text_rotation = text_rotation + 180
                vertical_align = 'top'
            plt.text(np.radians(label_angle), 105, r'' + label_name, ha='center', va=vertical_align,
                     transform=ax.transData, rotation=text_rotation, rotation_mode='anchor', fontsize=8)
            metric_num += 1

    ax.set_ylim([0, 100])

    return ax


def showMetricsRadar(players_df, player_name, player_team, metrics_list, metrics_colors, fig, gs, row_start, row_end,
                       col_start, col_end, show_axis):
    return showPolarGraph(players_df, player_name, player_team, metrics_list, metrics_colors, fig, gs, row_start, row_end,
                       col_start, col_end, show_axis=show_axis)


def showPassingRadar(players_df, player_name, player_team, metrics_list, fig, gs, row_start, row_end, col_start, col_end):
    ax = showPolarGraph(players_df, player_name, player_team, metrics_list, [1, 1, 1], fig, gs, row_start,
                          row_end, col_start, col_end, show_axis=False, theta_offset=2)
    ax.set_thetamin(0)
    ax.set_thetamax(180)

    return ax


def showAttributeRadar(players_df, player_name, player_team, metrics_list, metrics_colors, fig, gs, row_start, row_end,
                       col_start, col_end, show_axis, rating_label='Overall Rating'):
    return showPolarGraph(players_df, player_name, player_team, metrics_list, metrics_colors, fig, gs, row_start,
                          row_end, col_start, col_end, theta_offset=1.6, show_axis=show_axis, label_angle_offset=20,
                          rating_label=rating_label)


def showShotMap(shots_df, fig, gs, row, column):
    ax = fig.add_subplot(gs[row, column])
    img = plt.imread("shotmap.JPG")
    ax.imshow(img, extent=[0, 1, 0.7, 1])

    for index, shot in shots_df.iterrows():
        if shot['result'] == 'Goal':
            plt.scatter(shot['y'], shot['x'], color='#74c69d', s=shot['xG'] * 200, edgecolor='#74c69d', alpha=0.4)
        elif shot['result'] == 'SavedShot':
            plt.scatter(shot['y'], shot['x'], color='#2d6aa7', s=shot['xG'] * 200, edgecolor='#2d6aa7', alpha=0.4)
        else:
            plt.scatter(shot['y'], shot['x'], color='#ff4d4d', s=shot['xG'] * 200, edgecolor='#ff4d4d', alpha=0.4)

    ax.set_ylim([0.7, 1])
    ax.set_xticks([])
    ax.set_yticks([])
    return ax
