import pandas as pd
import numpy as np

from .variables import *
from .custom_logging import get_logger

log = get_logger("preproc")
log.disabled = False


def preprocess_data(targetCsv, features_mode=COUNT_ONLY, corr_threshold=0.9):
    df = targetCsv

    if features_mode == COUNT_ONLY:
        log.info("Removing the features according to the mode: COUNT_ONLY")
        df = df.drop(columns=COUNT_ONLY_EXCLUDED_COLS)
    elif features_mode == COUNT_MEAN:
        log.info("Removing the features according to the mode: COUNT_MEAN")
        df = df.drop(columns=COUNT_MEAN_ONLY_EXCLUDED_COLS)
    elif features_mode == COUNT_MEAN_SKEW:
        log.info("Removing the features according to the mode: COUNT_MEAN_SKEW")
        df = df.drop(columns=COUNT_MEAN_SKEW_ONLY_EXCLUDED_COLS)

    # Drop 0 variances features
    variances = df.var()
    zero_var_cols = variances[variances == 0].index
    log.info("Removing the features having variance = 0 ...")

    df = df.drop(columns=zero_var_cols)

    log.info("The following features were removed: \n" + ', '.join(zero_var_cols))

    # Drop correlated features
    corr_mat = df.corr()
    unsigned_corr_mat = corr_mat.abs()
    mat_upper_triangle = (unsigned_corr_mat.where(np.triu(np.ones(unsigned_corr_mat.shape), k=1).astype(np.bool))
                          .stack()
                          .sort_values(ascending=False))
    highly_correlated_pairs = mat_upper_triangle[mat_upper_triangle >= corr_threshold]

    highly_correlated_cols = []
    for col_pair in highly_correlated_pairs.index:
        # When running the outlierfinder with a small amount of matches it can happen that the id column is highly correlated with another column and gets dropped
        # We need it later though and correlation to the id column is kind of whacky and nonsensical anyways, so we prevent it here from happening
        if col_pair[0].upper() != "ID":
            highly_correlated_cols.append(col_pair[0])

    log.info("Removing the features having high correlation (corr > " + str(corr_threshold) + ") ...")

    df = df.drop(columns=highly_correlated_cols)

    log.info("The following features were removed: \n" +
             "\n".join([col_pair[0] + " (correlates with " + col_pair[1] + ")" for col_pair in
                        highly_correlated_pairs.index]))

    return df
