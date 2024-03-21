from abc import ABC, abstractmethod

import pandas as pd

from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
from sklearn.metrics import plot_roc_curve
from sklearn.metrics import balanced_accuracy_score, accuracy_score, f1_score, precision_score, recall_score
from sklearn.metrics import average_precision_score, fowlkes_mallows_score, confusion_matrix
from sklearn.metrics import precision_recall_curve, auc
from sklearn.metrics import plot_precision_recall_curve

from .preprocessing import preprocess_data
from .outlier_detection import *
from .custom_logging import get_logger
from .variables import *

log = get_logger("eval")
log.disabled = False

t_values = [90, 100, 110, 120, 150, 200]  # default = 100 |
psi_values = [200, 256, 300, 350, "auto"]  # default = "auto" | opt = 256
k_values = [10, 15, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 150,170,200, 250, 270, 290, 320]  # default = 20

if_random_state = 1


def get_y(df, y_file):
    df_labelled = pd.read_csv(y_file)
    outliers = df_labelled.loc[df_labelled['outlier'] == -1]
    outlier_ids = outliers['id'].tolist()
    df_y = df.copy()
    df_y['outlier'] = 1
    df_y.loc[df_y['id'].isin(outlier_ids), 'outlier'] = -1

    return df_y['outlier'], df_y['outlier'].value_counts(normalize=True)[-1]


def get_y_df(df, y_file):
    df_labelled = pd.read_csv(y_file)
    outliers = df_labelled.loc[df_labelled['outlier'] == -1]
    outlier_ids = outliers['id'].tolist()
    df_y = df.copy()
    df_y['outlier'] = 1
    df_y.loc[df_y['id'].isin(outlier_ids), 'outlier'] = -1

    return df_y, df_y['outlier'].value_counts(normalize=True)[-1]


class Evaluation(ABC):
    def __init__(self):
        self.y_pred = dict()
        self.roc_auc = dict()
        self.pr_auc = dict()
        self.training_time = dict()
        self.fpr = dict()
        self.tpr = dict()
        self.roc_thresh = dict()
        self.sp = dict()
        self.ps = dict()  # precision score
        self.rs = dict()  # recall score
        self.ap = dict()  # average precision
        self.f1 = dict()
        self.fmi = dict()  # geometric mean
        self.p = dict()  # precision values for pr curve
        self.r = dict()  # recall values for pr curve
        self.pr_thresh = dict()  # threshold values for pr curve
        self.cm = dict()  # confusion matrix
        self.cm_norm = dict()  # confusion matrix normlized
        self.params_combinations = None
        self.algorithm = None

    @abstractmethod
    def make_params_combinations(self) -> dict:
        pass

    def log_results(self):
        for key in self.get_keys():
            self.log_result(key)

    def log_results_latex_table_rows(self):
        for key in self.get_keys():
            self.log_result_latex_table_row(key)

    @abstractmethod
    def log_result(self, key) -> None:
        pass

    @abstractmethod
    def log_result_latex_table_row(self, key) -> None:
        pass

    def evaluate(self, X, y, contamination=None):
        log.info(" Starting evaluation: Total count=%d with contamination=%.4f" % (y.shape[0], contamination))

        for key, param in self.params_combinations.items():
            if contamination is not None:
                param['contamination'] = contamination
            self.y_pred[key], self.training_time[key] = classify_outliers(X, algorithm=self.algorithm,
                                                                          model_params=param)
            self.roc_auc[key] = roc_auc_score(y, self.y_pred[key]['score'])
            self.f1[key] = f1_score(y, self.y_pred[key]['outlier'])
            self.fpr[key], self.tpr[key], self.roc_thresh[key] = roc_curve(y, self.y_pred[key]['score'])
            self.ap[key] = average_precision_score(y, self.y_pred[key]['outlier'])
            self.p[key], self.r[key], self.pr_thresh[key] = precision_recall_curve(y, self.y_pred[key]['score'])
            self.pr_auc[key] = auc(self.r[key], self.p[key])
            self.fmi[key] = fowlkes_mallows_score(y, self.y_pred[key]['outlier'])
            self.ps[key] = precision_score(y, self.y_pred[key]['outlier'])
            self.rs[key] = recall_score(y, self.y_pred[key]['outlier'])
            self.cm[key] = confusion_matrix(y, self.y_pred[key]['outlier'])
            self.cm_norm[key] = confusion_matrix(y, self.y_pred[key]['outlier'], normalize='true')
            tn, fp, fn, tp = self.cm[key].ravel()
            self.sp[key] = tn / (tn + fp)

    def get_opt_params(self, attr_name):
        if attr_name not in ['roc_auc', 'pr_auc', 'f1', 'ap', 'fmi', 'ps', 'rs', 'sp']:
            raise AttributeError('%s is not a valid attribute to select the optimal parameter' % attr_name)

        attr = getattr(self, attr_name)
        return max(attr, key=attr.get)

    def get_keys(self):
        return self.params_combinations.keys()


class IForestEvaluation(Evaluation):

    def __init__(self, random_state=2):
        super(IForestEvaluation, self).__init__()
        self.algorithm = IF
        self.random_state = random_state
        self.params_combinations = self.make_params_combinations()

    def make_params_combinations(self):
        params = dict()
        for t in t_values:
            for psi in psi_values:
                key = '%s|%s' % (str(t), str(psi))
                params[key] = {'n_estimators': t, 'max_samples': psi, 'contamination': 0.01,
                               'random_state': self.random_state}

        return params

    def log_result(self, key, note=''):
        log.info('Isolation Forest %s for t=%s and psi=%s:| ROC AUC=%.5f | PR AUC=%.5f | SP=%.5f | F1=%.5f | FMI=%.5f '
                 '| runtime=%.5fs |' % (
                     note,
                     str(self.params_combinations[key]['n_estimators']),
                     str(self.params_combinations[key]['max_samples']),
                     self.roc_auc[key], self.pr_auc[key], self.sp[key], self.f1[key], self.fmi[key],
                     self.training_time[key]))

    def log_result_latex_table_row(self, key):
        print('$t=%s$ | $\\psi=%s$ & %.5f & %.5f & %.5f & %.5f & %.5f & %.5f \\\\ \n \\hline' % (
            str(self.params_combinations[key]['n_estimators']),
            str(self.params_combinations[key]['max_samples']),
            self.roc_auc[key], self.pr_auc[key], self.sp[key], self.f1[key], self.fmi[key],
            self.training_time[key]))

    def get_opt_params(self, attr_name):
        opt_params = super(IForestEvaluation, self).get_opt_params(attr_name)
        return tuple(opt_params.split("|"))


class LOFEvaluation(Evaluation):

    def __init__(self):
        super(LOFEvaluation, self).__init__()
        self.algorithm = LOF
        self.params_combinations = self.make_params_combinations()

    def make_params_combinations(self):
        params = dict()
        for k in k_values:
            params[k] = {'n_neighbors': k, 'contamination': 0.01}

        return params

    def log_result(self, key, note=''): \
            log.info('Local Outlier Factor %s for k=%d:| ROC AUC=%.5f | PR AUC=%.5f | SP=%.5f | F1=%.5f | FMI=%.5f | '
                     'runtime=%.5fs |' % (
                         note,
                         self.params_combinations[key]['n_neighbors'], self.roc_auc[key], self.pr_auc[key],
                         self.sp[key],
                         self.f1[key], self.fmi[key], self.training_time[key]))

    def log_result_latex_table_row(self, key):
        print('$k=%d$ & %.5f & %.5f & %.5f & %.5f & %.5f & %.5f \\\\ \n \\hline' % (
            self.params_combinations[key]['n_neighbors'], self.roc_auc[key], self.pr_auc[key],
            self.sp[key],
            self.f1[key], self.fmi[key], self.training_time[key]))


if __name__ == '__main__':
    contamination = 0.01
    if_eval = IForestEvaluation()
    lof_eval = LOFEvaluation()

    X = preprocess_data(DATASET_LOCATION, COUNT_ONLY)
    y, _ = get_y_df(X, Y_DATASET_LOCATION)

    if_eval.evaluate(X, y['outlier'], contamination)
    lof_eval.evaluate(X, y['outlier'], contamination)

    opt_t, opt_psi = if_eval.get_opt_params('fmi')
    opt_k = lof_eval.get_opt_params('fmi')
