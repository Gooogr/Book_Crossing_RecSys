"""Helper function for data preparation stage"""

import numbers
from typing import Optional

import pandas as pd


def auto_opt_pd_dtypes(df_: pd.DataFrame, inplace=False) -> Optional[pd.DataFrame]:
    """
    Automatically downcast Number dtypes for minimal possible, will not touch other
    dtypes (datetime, str, object, etc).
    Args:
    - df_ (pd.DataFrame): Input dataframe
    - inplace (bool): if `False`, will return a copy of input dataset
    Return:
    - `None` if `inplace=True` or dataframe if `inplace=False`
    """
    df = df_ if inplace else df_.copy()
    for col in df.columns:
        # integers
        if issubclass(df[col].dtypes.type, numbers.Integral):
            # unsigned integers
            if df[col].min() >= 0:
                df[col] = pd.to_numeric(df[col], downcast="unsigned")
            # signed integers
            else:
                df[col] = pd.to_numeric(df[col], downcast="integer")
        # other real numbers
        elif issubclass(df[col].dtypes.type, numbers.Real):
            df[col] = pd.to_numeric(df[col], downcast="float")

    if not inplace:
        return df
