import requests
import json
import warnings
import logging
import numpy as np

from scipy import stats

warnings.filterwarnings('ignore', message='Unverified HTTPS request')

MATCH_BASE_URL = 'https://jenkins.informatik.fb2.hs-intern.de/robocup/match/'
LAST_NIGHT_CSV_URL = 'https://jenkins.informatik.fb2.hs-intern.de/robocup/lastNightsCSV'
# COMMITS_URL = 'https://jenkins.informatik.fb2.hs-intern.de/robocup/commit/' --> revelant commit: 1354ef85760bd559aff07265910987c8b1bd3be5

CSV_FILENAME = "../data/dataset1.csv"

CSV_KEYS = ['id',  # add count
            'tackles_r_mean', 'tackles_r_skew', 'tackles_r_kurtosis', 'tackles_r_var', 'tackles_r_median',
            'tackles_r_count',
            'offsides_r_mean', 'offsides_r_skew', 'offsides_r_kurtosis', 'offsides_r_var', 'offsides_r_median',
            'offsides_r_count',
            'total_shots_l',
            'yellow_cards_r_mean', 'yellow_cards_r_skew', 'yellow_cards_r_kurtosis', 'yellow_cards_r_var',
            'yellow_cards_r_median', 'yellow_cards_r_count',
            'fouls_l_mean', 'fouls_l_skew', 'fouls_l_kurtosis', 'fouls_l_var', 'fouls_l_median', 'fouls_l_count',
            'shots_on_target_l',
            'corners_l_mean', 'corners_l_skew', 'corners_l_kurtosis', 'corners_l_var', 'corners_l_median',
            'corners_l_count',
            'total_shots_r',
            'goals_r_mean', 'goals_r_skew', 'goals_r_kurtosis', 'goals_r_var', 'goals_r_median', 'goals_r_count',
            'shots_on_target_r',
            'passes_r',
            'possession_r',
            'pass_chains_r_count',  # no timestamps => number of passes in a chain
            'tackles_l_mean', 'tackles_l_skew', 'tackles_l_kurtosis', 'tackles_l_var', 'tackles_l_median',
            'tackles_l_count',
            'possession_l',
            'goals_l_mean', 'goals_l_skew', 'goals_l_kurtosis', 'goals_l_var', 'goals_l_median', 'goals_l_count',
            'corners_r_mean', 'corners_r_skew', 'corners_r_kurtosis', 'corners_r_var', 'corners_r_median',
            'corners_r_count',
            'ball_on_side_r',
            'red_cards_r_mean', 'red_cards_r_skew', 'red_cards_r_kurtosis', 'red_cards_r_var', 'red_cards_r_median',
            'red_cards_r_count',
            'red_cards_l_mean', 'red_cards_l_skew', 'red_cards_l_kurtosis', 'red_cards_l_var', 'red_cards_l_median',
            'red_cards_l_count',
            'passes_l',
            'yellow_cards_l_mean', 'yellow_cards_l_skew', 'yellow_cards_l_kurtosis', 'yellow_cards_l_var',
            'yellow_cards_l_median', 'yellow_cards_l_count',
            'free_kicks_r_mean', 'free_kicks_r_skew', 'free_kicks_r_kurtosis', 'free_kicks_r_var',
            'free_kicks_r_median', 'free_kicks_r_count',
            'free_kicks_l_mean', 'free_kicks_l_skew', 'free_kicks_l_kurtosis', 'free_kicks_l_var',
            'free_kicks_l_median', 'free_kicks_l_count',
            'fouls_r_mean', 'fouls_r_skew', 'fouls_r_kurtosis', 'fouls_r_var', 'fouls_r_median', 'fouls_r_count',
            'offsides_l_mean', 'offsides_l_skew', 'offsides_l_kurtosis', 'offsides_l_var', 'offsides_l_median',
            'offsides_l_count',
            'ball_on_side_l',
            'pass_chains_l_count']  # no timestamps => number of passes in a chain

RELEVANT_JSON_KEYS = ['_id',
                      'tackles_r',
                      'offsides_r',
                      'total_shots_l',
                      'yellow_cards_r',
                      'fouls_l',
                      'shots_on_target_l',
                      'corners_l',
                      'total_shots_r',
                      'goals_r',
                      'shots_on_target_r',
                      'passes_r',
                      'possession_r',
                      'pass_chains_r',
                      'tackles_l',
                      'possession_l',
                      'goals_l',
                      'corners_r',
                      'ball_on_side_r',
                      'red_cards_r',
                      'red_cards_l',
                      'passes_l',
                      'yellow_cards_l',
                      'free_kicks_r',
                      'free_kicks_l',
                      'fouls_r',
                      'offsides_l',
                      'ball_on_side_l',
                      'pass_chains_l']

DEBUG = False
SAMPLE_ID_START = 100000
SAMPLE_ID_FINISH = 101000


def main():
    # noinspection PyArgumentList
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            # logging.FileHandler("debug.log"),
            logging.StreamHandler()
        ]
    )

    with open(CSV_FILENAME, 'wb') as file:
        csv_header = ','.join(CSV_KEYS) + '\n'
        file.write(str.encode(csv_header))

        sample_id = SAMPLE_ID_START
        consecutive_missing_samples_count = 0
        missing_samples_count = 0
        while True:
            response = requests.get(MATCH_BASE_URL + str(sample_id), verify=False)
            json_sample = json.loads(response.text)

            if 'error' in json_sample and json_sample['error'] == 404:
                logging.warning('Could not retrieve sample for ID: ' + str(sample_id))
                consecutive_missing_samples_count += 1
                sample_id += 1
                missing_samples_count += 1
                continue

            if consecutive_missing_samples_count > 10 or sample_id > SAMPLE_ID_FINISH:
                logging.info('All samples have been processed.')
                break

            logging.info('ID: ' + str(sample_id))
            logging.debug("JSON:" + str(json_sample))

            line = ''
            for key in RELEVANT_JSON_KEYS:
                if isinstance(json_sample[key], list):
                    if 'pass_chains' in key:
                        line += str(len(json_sample[key])) + ','
                        continue

                    if len(json_sample[key]) == 0:
                        json_sample[key] = [0]
                        count = 0

                    else:
                        count = len(json_sample[key])

                    mean = np.mean(json_sample[key])
                    skew = stats.skew(json_sample[key])
                    kurtosis = stats.kurtosis(json_sample[key])
                    var = np.var(json_sample[key])
                    median = np.median(json_sample[key])

                    line += ','.join([str(val) for val in [mean, skew, kurtosis, var, median, count]]) + ','

                else:
                    line += str(json_sample[key]) + ','

            logging.debug("CSV:" + line)

            file.write(str.encode(line[:-1] + '\n'))

            sample_id += 1
            consecutive_missing_samples_count = 0

        print('finished Crawling')
        print('Number of missing values: ' + str(missing_samples_count))


def download_file(url=LAST_NIGHT_CSV_URL):
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True, verify=False) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename