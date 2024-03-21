import time

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler

from sklearn.neighbors import LocalOutlierFactor
from sklearn.ensemble import IsolationForest

from OutlierFinder.core.custom_logging import get_logger

log = get_logger("outlier_detection")
log.disabled = False

IF = 0
LOF = 1

algorithms_str = {
    IF: "isolation_forest",
    LOF: "LOF"
}

# These optimal parameters were deducted from the evaluation
if_opt_model_params = {'contamination': 0.01, 'max_samples': 256, 'n_estimators': 100}
lof_opt_model_params = {'contamination': 0.01, 'n_neighbors': 150}


def classify_outliers(df, algorithm, model_params):
    df_ids = df["id"]
    df = df.drop(columns=["id"])
    log.info("Algorithm: " + algorithms_str[algorithm])

    if algorithm == IF:
        df_pred, runtime = isolation_forest(df, model_params)
    elif algorithm == LOF:
        df_pred, runtime = lof(df, model_params)
    else:
        raise RuntimeError("algorithm not supported")

    df_pred.insert(0, "id", df_ids)
    return df_pred, runtime


def isolation_forest(df, kwargs):
    """ Outliers are marked with -1 and inliers with 1 """

    model = IsolationForest(**kwargs)

    log.info("Standardizing the dataset:")
    df_norm = standardize(df)

    log.info("fitting the model")
    t0 = time.time()
    model.fit(df_norm)
    t1 = time.time()

    df_pred = df.copy()
    log.info("Classifying outliers")
    df_pred['score'] = model.decision_function(df_norm)
    df_pred['outlier'] = model.predict(df_norm)

    return df_pred, t1 - t0


def lof(df, kwargs):
    """ Outliers are marked with -1 and inliers with 1 """

    model = LocalOutlierFactor(**kwargs)

    log.info("Standardizing the dataset:")
    df_norm = standardize(df)

    df_pred = df.copy()

    log.info("Fitting the model and classifying outliers")
    t0 = time.time()
    df_pred['outlier'] = model.fit_predict(df_norm)
    t1 = time.time()
    df_pred['score'] = model.negative_outlier_factor_

    return df_pred, t1 - t0


def standardize(df):
    return (df - df.mean()) / df.std()


def normalize(df):
    scaler = MinMaxScaler()
    return scaler.fit_transform(df)