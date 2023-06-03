def getPolarChartPositionMetrics(position):
    if position == "CB":
        return [
                   'Defensive duels per 90',
                   'PAdj Interceptions',
                   'Shots blocked per 90',
                   'Aerial duels per 90',
                   'Aerial duels won, %',
                   'Progressive runs per 90',
                   'Progressive passes per 90',
                   'Forward passes per 90',
                   'Accurate forward passes, %',
                   'Deep completions per 90',
                   'Passes to final third per 90',
                   'Accurate passes to final third, %',
                   'Smart passes per 90',
                   'Shot assists per 90',
                   'Key passes per 90'
               ], [5, 2, 3, 5]
    elif position == "WB":
        return [
                   'Successful defensive actions per 90',
                   'PAdj Interceptions',
                   'Aerial duels per 90',
                   'Aerial duels won, %',
                   'Crosses per 90',
                   'Accurate crosses, %',
                   'Crosses to goalie box per 90',
                   'Deep completions per 90',
                   'xA per 90',
                   'Shot assists per 90',
                   'Key passes per 90',
                   'Progressive runs per 90',
                   'Dribbles per 90',
                   'Successful dribbles, %',
                   'Progressive passes per 90'
               ], [4, 4, 3, 4]
    elif position == "CM":
        return [
                   'Accurate Progressive Passes per 90',
                   'Accurate Forward Passes per 90',
                   'Passes to final third per 90',
                   'Received passes per 90',
                   'xA per 90',
                   'Shot assists per 90',
                   'Key passes per 90',
                   'Through passes per 90',
                   'Deep completions per 90',
                   'Successful defensive actions per 90',
                   'Defensive duels won, %',
                   'PAdj Interceptions',
                   'Progressive runs per 90',
                   'Shots per 90',
                   'xG per 90'
               ], [4, 5, 3, 3]
    else:
        return [
                   'Non-penalty goals per 90',
                   'xG per 90',
                   'Shots per 90',
                   'Shots on target, %',
                   'xA per 90',
                   'Shot assists per 90',
                   'Key passes per 90',
                   'Dribbles per 90',
                   'Successful dribbles, %',
                   'Progressive runs per 90',
                   'Touches in box per 90',
                   'Passes to penalty area per 90',
                   'Aerial duels per 90',
                   'Aerial duels won, %',
                   'PAdj Interceptions'
               ], [4, 3, 3, 2, 3]


def getScatterPlotMetrics(position):
    if position == "CB":
        return [
            ['Aerial duels', 'Aerial duels per 90', 'Aerial duels won, %'],
            ['Defending', 'PAdj Interceptions', 'Defensive duels per 90'],
            ['Forward passes', 'Forward passes per 90', 'Accurate forward passes, %'],
            ['Progressive passes/runs', 'Progressive passes per 90', 'Progressive runs per 90']
        ]
    elif position == "WB":
        return [
            ['Defending', 'PAdj Interceptions', 'Defensive duels per 90'],
            ['Dribbling', 'Dribbles per 90', 'Successful dribbles, %'],
            ['Crossing', 'Crosses per 90', 'Accurate crosses, %'],
            ['Progressive passes/runs', 'Progressive passes per 90', 'Progressive runs per 90']
        ]
    elif position == "CM":
        return [
            ['Progressive passes/runs', 'Progressive passes per 90', 'Progressive runs per 90'],
            ['Defending', 'PAdj Interceptions', 'Defensive duels per 90'],
            ['Forward passes', 'Forward passes per 90', 'Accurate forward passes, %'],
            ['xG vs xA', 'xA per 90', 'xG per 90']
        ]
    else:
        return [
            ['Goals vs xG', 'xG per 90', 'Goals per 90'],
            ['Shooting', 'Shots per 90', 'Shots on target, %'],
            ['Aerial duels', 'Aerial duels per 90', 'Aerial duels won, %'],
            ['Dribbling', 'Dribbles per 90', 'Successful dribbles, %']
        ]


def attributeMetrics(attribute):
    attribute_metrics = {
        'defensive_ability': [
            'Defensive duels per 90',
            'Defensive duels won, %'
        ],
        'defensive_positioning': [
            'Shots blocked per 90',
            'PAdj Interceptions'
        ],
        'aerial_ability': [
            'Aerial duels per 90',
            'Aerial duels won, %'
        ],
        'ball_carrying': [
            'Progressive runs per 90',
            'Accelerations per 90'
        ],
        'ball_retention': [
            'Accurate Passes per 90',
            'Passes per 90',
            'Long passes per 90',
            'Accurate Long Passes per 90',
            'Received passes per 90'
        ],
        'ball_playing': [
            'Accurate Passes per 90',
            'Forward passes per 90',
            'Accurate Forward Passes per 90',
            'Forward Passes %',
            'Progressive passes per 90',
            'Accurate Progressive Passes per 90',
            'Progressive Passes %'
        ],
        'attacking_entries': [
            'Accurate Passes to final third per 90',
            'Passes to final third per 90',
            'Deep completions per 90'
        ],
        'attacking_creativity': [
            'xA per 90',
            'Assists per 90',
            'Shot assists per 90',
            'Key passes per 90',
            'Through passes per 90'
        ],
        'crossing': [
            'Crosses per 90',
            'Accurate crosses, %',
            'Crosses to goalie box per 90',
            'Deep completed crosses per 90'
        ],
        'attacking_threat': [
            'xG per 90',
            'Non-penalty goals per 90',
            'Head goals per 90',
            'Shots per 90'
        ],
        'shooting': [
            'Shots per 90',
            'Shots on target, %'
        ],
        'holdup_play': [
            'Received long passes per 90',
            'Fouls suffered per 90',
            'Short / medium passes per 90',
            'Accurate short / medium passes, %'
        ],
        'dribbling': [
            'Dribbles per 90',
            'Successful dribbles, %'
        ],
        'box_entries': [
            'Touches in box per 90',
            'Passes to penalty area per 90',
            'Accurate passes to penalty area, %',
            'Deep completions per 90'
        ]
    }

    if attribute == "all":
        all_metrics = ['Minutes played']
        for key, attr in attribute_metrics.items():
            for metric in attr:
                all_metrics.append(metric)
        return all_metrics
    elif attribute in attribute_metrics:
        return attribute_metrics[attribute]
    else:
        return 'none'


def attributeMetricsWeights(position):
    attribute_metric_weights = {
        'CB BP': {
            'Minutes played_zscore': 0.125,
            'defensive_ability': 0.1,
            'defensive_positioning': 0.125,
            'aerial_ability': 0.1,
            'ball_carrying': 0.2,
            'ball_playing': 0.2,
            'attacking_entries': 0.1,
            'attacking_threat': 0.05,
        },
        'CB BW': {
            'Minutes played_zscore': 0.125,
            'defensive_ability': 0.25,
            'defensive_positioning': 0.2,
            'aerial_ability': 0.2,
            'ball_carrying': 0.05,
            'ball_playing': 0.075,
            'attacking_entries': 0.05,
            'attacking_threat': 0.05,
        },
        'WB BP': {
            'Minutes played_zscore': 0.125,
            'defensive_ability': 0.1,
            'defensive_positioning': 0.1,
            'crossing': 0.15,
            'ball_carrying': 0.15,
            'dribbling': 0.15,
            'attacking_creativity': 0.1,
            'attacking_entries': 0.125,
        },
        'WB BW': {
            'Minutes played_zscore': 0.125,
            'defensive_ability': 0.2,
            'defensive_positioning': 0.2,
            'crossing': 0.1,
            'ball_carrying': 0.1,
            'dribbling': 0.1,
            'attacking_creativity': 0.075,
            'attacking_entries': 0.1,
        },
        'CM BP': {
            'Minutes played_zscore': 0.125,
            'ball_retention': 0.1,
            'ball_playing': 0.15,
            'ball_carrying': 0.15,
            'attacking_creativity': 0.15,
            'attacking_entries': 0.15,
            'attacking_threat': 0.1,
            'defensive_positioning': 0.075,
        },
        'CM BW': {
            'Minutes played_zscore': 0.125,
            'defensive_ability': 0.15,
            'defensive_positioning': 0.2,
            'aerial_ability': 0.125,
            'ball_carrying': 0.1,
            'ball_playing': 0.1,
            'ball_retention': 0.15,
            'attacking_entries': 0.05,
        },
        'AM BC': {
            'Minutes played_zscore': 0.125,
            'ball_carrying': 0.2,
            'dribbling': 0.15,
            'attacking_threat': 0.1,
            'attacking_creativity': 0.1,
            'attacking_entries': 0.15,
            'box_entries': 0.125,
            'defensive_positioning': 0.05,
        },
        'AM C': {
            'Minutes played_zscore': 0.125,
            'ball_carrying': 0.1,
            'dribbling': 0.1,
            'attacking_threat': 0.125,
            'attacking_creativity': 0.2,
            'attacking_entries': 0.15,
            'box_entries': 0.15,
            'defensive_positioning': 0.05,
        },
        'ST TM': {
            'Minutes played_zscore': 0.125,
            'aerial_ability': 0.15,
            'holdup_play': 0.175,
            'shooting': 0.1,
            'box_entries': 0.1,
            'dribbling': 0.1,
            'attacking_entries': 0.15,
            'ball_retention': 0.1,
        },
        'ST A': {
            'Minutes played_zscore': 0.125,
            'attacking_threat': 0.2,
            'shooting': 0.15,
            'attacking_creativity': 0.1,
            'box_entries': 0.15,
            'dribbling': 0.1,
            'ball_carrying': 0.1,
            'defensive_ability': 0.075,
        }
    }

    if position in attribute_metric_weights:
        return attribute_metric_weights[position]
    else:
        return 'none'
