# data_processor.py
import logging
import pandas as pd

logger = logging.getLogger(__name__)


def remove_duplicates(df):
    """Remove duplicate rows."""
    before = len(df)
    df = df.drop_duplicates()
    logger.debug(f"remove_duplicates: {before} → {len(df)} rows")
    return df


def handle_missing(df, axis="rows"):
    """Drop rows or columns containing missing values."""
    if axis == "rows":
        before = len(df)
        df = df.dropna(axis=0)
        logger.debug(f"handle_missing: {before} → {len(df)} rows")
    elif axis == "columns":
        before = df.shape[1]
        df = df.dropna(axis=1)
        logger.debug(f"handle_missing: {before} → {df.shape[1]} columns")
    else:
        logger.error(f"Unsupported axis: {axis}")
        raise ValueError(f"Unsupported axis: {axis}")
    return df


def remove_outliers(df, columns, method, threshold):
    """Remove outliers from the specified numeric columns."""
    if method not in ("iqr", "zscore"):
        logger.error(f"Unsupported outlier method: {method}")
        raise ValueError(f"Unsupported outlier method: {method}")

    for col in columns:
        if col not in df.columns:
            logger.warning(f"Column not found: {col}")
            continue
        if not pd.api.types.is_numeric_dtype(df[col]):
            logger.warning(f"Column is not numeric: {col}")
            continue

        before = len(df)

        if method == "iqr":
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            lower = q1 - threshold * iqr
            upper = q3 + threshold * iqr
            keep = df[col].between(lower, upper) | df[col].isna()
        else:  # zscore
            mean = df[col].mean()
            std = df[col].std()
            lower = mean - threshold * std
            upper = mean + threshold * std
            if std == 0 or pd.isna(std):
                keep = pd.Series(True, index=df.index)
            else:
                z = (df[col] - mean) / std
                keep = (z.abs() <= threshold) | df[col].isna()

        df = df[keep]
        logger.debug(
            f"{col}: method={method}, threshold={threshold}, "
            f"lower={lower}, upper={upper}, removed={before - len(df)}"
        )

    return df


def process_data(df, config):
    """Apply the processing steps enabled in the configuration."""
    settings = config["processing"]

    if settings["remove_duplicates"]:
        df = remove_duplicates(df)

    missing = settings["missing"]
    if missing["enabled"]:
        df = handle_missing(df, axis=missing["axis"])

    outliers = settings["outliers"]
    if outliers["enabled"]:
        df = remove_outliers(
            df,
            columns=outliers["columns"],
            method=outliers["method"],
            threshold=outliers["threshold"],
        )

    return df


def create_cleaning_report(df_before, df_after):
    """Return a dictionary summarizing the cleaning results."""
    rows_before, cols_before = df_before.shape
    rows_after, cols_after = df_after.shape
    return {
        "rows_before": rows_before,
        "rows_after": rows_after,
        "rows_removed": rows_before - rows_after,
        "columns_before": cols_before,
        "columns_after": cols_after,
        "columns_removed": cols_before - cols_after,
    }