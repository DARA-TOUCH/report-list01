import pandas as pd
from .static_object import COLUMN_LABELS
# from static_object import COLUMN_LABELS
import os

__all__ = ['GroupID', 'Stamp']

def _get_file_path(file_name: str):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.abspath(os.path.join(script_dir, '..', '..', 'staticfiles', 'excel', 'csv'))

    group_by_hs_file = os.path.join(data_dir, 'group_by_hs.csv')
    stamp_by_hs_file = os.path.join(data_dir, 'stamp_by_hs.csv')

    if file_name == 'group_by_hs_file':
        return group_by_hs_file
    
    if file_name == 'stamp_by_hs_file':
        return stamp_by_hs_file

class GroupID:
    """
        Class represent dataframe of Group
    """
    def __init__(self):
        group_by_hs_file = _get_file_path(file_name='group_by_hs_file')
        self.__df = pd.read_csv(
            group_by_hs_file,
            usecols=[COLUMN_LABELS["hs_code"], "group_id", "transaction"],
            dtype={COLUMN_LABELS["hs_code"]: str},
        )
        self.__IM = self.__df[self.__df["transaction"] == "IM"]
        self.__EX = self.__df[self.__df["transaction"] == "EX"]

    def get_dataframe(self):
        return self.__df


    def get_IM_dataframe(self):
        return self.__IM

    def get_EX_dataframe(self):
        return self.__EX


class Stamp:
    def __init__(self):
        stamp_by_hs_file = _get_file_path('stamp_by_hs_file')
        self.__df = pd.read_csv(
            stamp_by_hs_file, usecols=[0, 1, 2], dtype={"hs_code": str}
        )

    def get_dataframe(self):
        return self.__df

    def available_stamp(self):
        return [stamp for stamp in self.__df["stamp_kind"].unique() if pd.notna(stamp)]

    def available_stamp_by_short_description(self):
        stamp_in_short_des_ = [stamp_sort_des_ for stamp_sort_des_ in self.__df['sort_des_'].unique()]
        return sorted(stamp_in_sort_des_)