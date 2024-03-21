import os
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

from .outlier_detection import *
from .custom_logging import get_logger
from .variables import *

""" This file is deprecated """

log = get_logger('analysis')
log.disabled = True

sns.set_theme(style='whitegrid')
cpal7 = sns.color_palette('coolwarm', n_colors=6, desat=0.2)
cpal2 = sns.color_palette('coolwarm', n_colors=2, desat=0.2)

algorithm = IF
algorithm_filename = algorithms_str[algorithm]

if_model_params = [
    {'contamination': 0.5, 'max_samples': 'auto'},
    {'contamination': 0.1, 'max_samples': 'auto'},
    {'contamination': 0.01, 'max_samples': 'auto'},
    {'contamination': 0.001, 'max_samples': 'auto'}
    # max_samples: default is 256, close to optimal
]

lof_model_params = [
    {'n_neighbors': 20, 'contamination': 0.1},
    {'n_neighbors': 20, 'contamination': 0.01},
    {'n_neighbors': 40, 'contamination': 0.1},
    {'n_neighbors': 40, 'contamination': 0.01},
    {'n_neighbors': 60, 'contamination': 0.1},
    {'n_neighbors': 60, 'contamination': 0.01}
]

features_modes = [
    COUNT_ONLY,
    COUNT_MEAN,
    COUNT_MEAN_SKEW
]

global feature_mode_filename
global model_param_filename

""" This file is deprecated """


def analyse_df(df_pred, filename=None, title=''):
    df_pred = df_pred.drop(columns=['id'])

    bins = [-0.20, -0.15, -0.10, -0.05, 0, 0.05, 0.1]
    df_pred['binned_score'] = pd.cut(df_pred['score'], bins)

    log.info('Plotting...')

    displot(df_pred, x='score', hue='outlier', kind='kde', cpal=cpal2, saveFig=True)
    scatterplot(data=df_pred, x='goals_l_count', y='goals_r_count', hue='binned_score', style='outlier',
                cpal=cpal7, saveFig=True)
    scatterplot(data=df_pred, x='goals_l_count', y='passes_l', hue='binned_score', style='outlier',
                cpal=cpal7, saveFig=True)
    scatterplot(data=df_pred, x='goals_r_count', y='passes_r', hue='binned_score', style='outlier',
                cpal=cpal7, saveFig=True)
    scatterplot(data=df_pred, x='goals_r_count', y='passes_l', hue='binned_score', style='outlier',
                cpal=cpal7, saveFig=True)
    scatterplot(data=df_pred, x='possession_l', y='shots_on_target_r', hue='binned_score', style='outlier',
                cpal=cpal7, saveFig=True)
    scatterplot(data=df_pred, x='possession_l', y='passes_r', hue='binned_score', style='outlier',
                cpal=cpal7, saveFig=True)
    scatterplot(data=df_pred, x='possession_l', y='shots_on_target_l', hue='binned_score', style='outlier',
                cpal=cpal7, saveFig=True)
    scatterplot(data=df_pred, x='possession_l', y='passes_l', hue='binned_score', style='outlier',
                cpal=cpal7, saveFig=True)
    pairplot(data=df_pred, hue='binned_score', cpal=cpal7, saveFig=True)

    log.info('Done')


def scatterplot(data, x, y, hue=None, style=None, title='', cpal=None, showFig=False, saveFig=False):
    log.info("Scatterplot: " + x + " | " + y)
    plot = sns.scatterplot(data=data, x=x, y=y, hue=hue, style=style, palette=cpal)
    plt.legend(fontsize='x-small', bbox_to_anchor=(1.01, 1), borderaxespad=0)
    if showFig:
        plt.suptitle(title, size=20)
        plt.show()
    if saveFig:
        plot.get_figure().savefig(get_filename("scatterplot", x=x, y=y), dpi=100)
    plt.close(plot.get_figure())


def displot(data, x, hue=None, kind='kde', title='', cpal=None, showFig=False, saveFig=False):
    log.info("Displot: " + x)
    plot = sns.displot(data=data, x=x, hue=hue, kind=kind, palette=cpal)
    plt.legend(fontsize='x-small', bbox_to_anchor=(1.01, 1), borderaxespad=0)
    if showFig:
        plt.suptitle(title, size=20)
        plt.show()
    if saveFig:
        plot.fig.savefig(get_filename("distplot", x=x), dpi=100)
    plt.close(plot.fig)


def pairplot(data, hue=None, title='', cpal=None, showFig=False, saveFig=False):
    log.info("Pairplot")
    plot = sns.pairplot(data, size=4, kind='scatter', diag_kind='hist', hue=hue, palette=cpal)
    plt.legend(fontsize='x-small', bbox_to_anchor=(1.01, 1), borderaxespad=0)
    if showFig:
        plt.suptitle(title, size=20)
        plt.show()
    if saveFig:
        plot.fig.savefig(get_filename("pairplot"), dpi=100)
    plt.close(plot.fig)


def get_filename(plot, x="", y=""):
    filename = plot + "_" + algorithm_filename + "_" + dict_to_title(model_param_filename) + "_" + FEATURE_MODES_STR[
        feature_mode_filename]
    if x:
        filename += "_" + x
    if y:
        filename += "_" + y

    return PLOTS_LOCATION + "\\" + filename + ".png"


def dict_to_title(dictionary):
    return '_'.join([str(k[0:4]) + '-' + str(i) for i, k in enumerate(dictionary)])


def start():
    for model_param in if_model_params:
        for features_mode in features_modes:
            log.info('Starting analysis for: Mode-' + str(features_mode) + ' | Model params: ' + str(model_param))

            df = preprocess_data(features_mode=features_mode)
            df_pred = classify_outliers(df, model_params=model_param)

            global model_param_filename
            model_param_filename = model_param
            global feature_mode_filename
            feature_mode_filename = features_mode
            analyse_df(df_pred)

            df_pred.loc[df_pred['outlier'] == -1].sort_values(by=['score']).to_csv(
                '../data/outliers%s.csv' % (int(model_param['contamination'] * 1000)))
            df_pred.loc[df_pred['outlier'] == 1].sort_values(by=['score']).to_csv(
                '../data/inliers%s.csv' % (int(model_param['contamination'] * 1000)))


def start_LOF(results_dir_path):
    df = preprocess_data(dataset="../data/dataset1.csv", features_mode=COUNT_ONLY)
    df_pred = classify_outliers(df, algorithm=LOF, model_params=lof_model_params[1])
    df_pred.sort_values(by=['score']).sort_values(by=['id']).to_csv(results_dir_path + '\\dataset1_lof.csv')
    write_summary(algorithms_str[LOF], lof_model_params[1], COUNT_ONLY, results_dir_path)


def start_IF(results_dir_path):
    df = preprocess_data(dataset="../data/dataset1.csv", features_mode=COUNT_ONLY)
    df_pred = classify_outliers(df, algorithm=IF, model_params=if_model_params[2])
    df_pred.sort_values(by=['score']).sort_values(by=['id']).to_csv(results_dir_path + '\\dataset1_if.csv')
    write_summary(algorithms_str[IF], if_model_params[2], COUNT_ONLY, results_dir_path)


def get_results_dir_path():
    if not os.path.exists(RESULTS_LOCATION):
        os.makedirs(RESULTS_LOCATION)

    timestamp_str = time.strftime("%Y%m%d%H%M%S")
    os.mkdir(RESULTS_LOCATION + "\\" + timestamp_str)

    return RESULTS_LOCATION + "\\" + timestamp_str


def write_summary(algo, params, features_mode, path):
    with open(path + "\\summary.txt", 'a+') as file:
        file.write('###' + algo + '###' + '\n')
        file.write('# features mode: ' + FEATURE_MODES_STR[features_mode] + "\n")
        file.write('# model params:\n')
        for k, v in params.items():
            file.write('\t' + str(k) + ' >>> ' + str(v) + '\n')
        file.write('\n')


if __name__ == '__main__':
    # start()
    results_dir_path = get_results_dir_path()
    start_LOF(results_dir_path)
    start_IF(results_dir_path)
    log.info("Finished")
