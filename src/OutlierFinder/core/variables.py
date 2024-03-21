PLOTS_LOCATION = "plots"
RESULTS_LOCATION = "results"
DATASET_LOCATION = "data/dataset1.csv"
Y_DATASET_LOCATION = "labelled_data//dataset1_if.csv"


# feature modes
COUNT_ONLY = 0
COUNT_MEAN = 1
COUNT_MEAN_SKEW = 2

FEATURE_MODES_STR = {
    COUNT_ONLY: 'count_only',
    COUNT_MEAN: 'count_mean',
    COUNT_MEAN_SKEW: 'count_mean_skew'
}

COUNT_ONLY_EXCLUDED_COLS = [
    'tackles_r_mean', 'tackles_r_skew', 'tackles_r_kurtosis', 'tackles_r_var', 'tackles_r_median',
    'offsides_r_mean', 'offsides_r_skew', 'offsides_r_kurtosis', 'offsides_r_var', 'offsides_r_median',
    'yellow_cards_r_mean', 'yellow_cards_r_skew', 'yellow_cards_r_kurtosis', 'yellow_cards_r_var',
    'yellow_cards_r_median',
    'fouls_l_mean', 'fouls_l_skew', 'fouls_l_kurtosis', 'fouls_l_var', 'fouls_l_median',
    'corners_l_mean', 'corners_l_skew', 'corners_l_kurtosis', 'corners_l_var', 'corners_l_median',
    'goals_r_mean', 'goals_r_skew', 'goals_r_kurtosis', 'goals_r_var', 'goals_r_median',
    'tackles_l_mean', 'tackles_l_skew', 'tackles_l_kurtosis', 'tackles_l_var', 'tackles_l_median',
    'goals_l_mean', 'goals_l_skew', 'goals_l_kurtosis', 'goals_l_var', 'goals_l_median',
    'corners_r_mean', 'corners_r_skew', 'corners_r_kurtosis', 'corners_r_var', 'corners_r_median',
    'red_cards_r_mean', 'red_cards_r_skew', 'red_cards_r_kurtosis', 'red_cards_r_var', 'red_cards_r_median',
    'red_cards_l_mean', 'red_cards_l_skew', 'red_cards_l_kurtosis', 'red_cards_l_var', 'red_cards_l_median',
    'yellow_cards_l_mean', 'yellow_cards_l_skew', 'yellow_cards_l_kurtosis', 'yellow_cards_l_var',
    'yellow_cards_l_median',
    'free_kicks_r_mean', 'free_kicks_r_skew', 'free_kicks_r_kurtosis', 'free_kicks_r_var', 'free_kicks_r_median',
    'free_kicks_r_median',
    'free_kicks_l_mean', 'free_kicks_l_skew', 'free_kicks_l_kurtosis', 'free_kicks_l_var', 'free_kicks_l_median',
    'free_kicks_l_median',
    'fouls_r_mean', 'fouls_r_skew', 'fouls_r_kurtosis', 'fouls_r_var', 'fouls_r_median',
    'offsides_l_mean', 'offsides_l_skew', 'offsides_l_kurtosis', 'offsides_l_var', 'offsides_l_median',
]

COUNT_MEAN_ONLY_EXCLUDED_COLS = [
    'tackles_r_skew', 'tackles_r_kurtosis', 'tackles_r_var', 'tackles_r_median',
    'offsides_r_skew', 'offsides_r_kurtosis', 'offsides_r_var', 'offsides_r_median',
    'yellow_cards_r_skew', 'yellow_cards_r_kurtosis', 'yellow_cards_r_var', 'yellow_cards_r_median',
    'fouls_l_skew', 'fouls_l_kurtosis', 'fouls_l_var', 'fouls_l_median',
    'corners_l_skew', 'corners_l_kurtosis', 'corners_l_var', 'corners_l_median',
    'goals_r_skew', 'goals_r_kurtosis', 'goals_r_var', 'goals_r_median',
    'tackles_l_skew', 'tackles_l_kurtosis', 'tackles_l_var', 'tackles_l_median',
    'goals_l_skew', 'goals_l_kurtosis', 'goals_l_var', 'goals_l_median',
    'corners_r_skew', 'corners_r_kurtosis', 'corners_r_var', 'corners_r_median',
    'red_cards_r_skew', 'red_cards_r_kurtosis', 'red_cards_r_var', 'red_cards_r_median',
    'red_cards_l_skew', 'red_cards_l_kurtosis', 'red_cards_l_var', 'red_cards_l_median',
    'yellow_cards_l_skew', 'yellow_cards_l_kurtosis', 'yellow_cards_l_var', 'yellow_cards_l_median',
    'free_kicks_r_skew', 'free_kicks_r_kurtosis', 'free_kicks_r_var', 'free_kicks_r_median', 'free_kicks_r_median',
    'free_kicks_l_skew', 'free_kicks_l_kurtosis', 'free_kicks_l_var', 'free_kicks_l_median', 'free_kicks_l_median',
    'fouls_r_skew', 'fouls_r_kurtosis', 'fouls_r_var', 'fouls_r_median',
    'offsides_l_skew', 'offsides_l_kurtosis', 'offsides_l_var', 'offsides_l_median',
]

COUNT_MEAN_SKEW_ONLY_EXCLUDED_COLS = [
    'tackles_r_kurtosis', 'tackles_r_var', 'tackles_r_median',
    'offsides_r_kurtosis', 'offsides_r_var', 'offsides_r_median',
    'yellow_cards_r_kurtosis', 'yellow_cards_r_var', 'yellow_cards_r_median',
    'fouls_l_kurtosis', 'fouls_l_var', 'fouls_l_median',
    'corners_l_kurtosis', 'corners_l_var', 'corners_l_median',
    'goals_r_kurtosis', 'goals_r_var', 'goals_r_median',
    'tackles_l_kurtosis', 'tackles_l_var', 'tackles_l_median',
    'goals_l_kurtosis', 'goals_l_var', 'goals_l_median',
    'corners_r_kurtosis', 'corners_r_var', 'corners_r_median',
    'red_cards_r_kurtosis', 'red_cards_r_var', 'red_cards_r_median',
    'red_cards_l_kurtosis', 'red_cards_l_var', 'red_cards_l_median',
    'yellow_cards_l_kurtosis', 'yellow_cards_l_var', 'yellow_cards_l_median',
    'free_kicks_r_kurtosis', 'free_kicks_r_var', 'free_kicks_r_median', 'free_kicks_r_median',
    'free_kicks_l_kurtosis', 'free_kicks_l_var', 'free_kicks_l_median', 'free_kicks_l_median',
    'fouls_r_kurtosis', 'fouls_r_var', 'fouls_r_median',
    'offsides_l_kurtosis', 'offsides_l_var', 'offsides_l_median',
]
