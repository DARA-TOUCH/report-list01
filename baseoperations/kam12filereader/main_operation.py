import pandas as pd
import numpy as np
import datetime
from pathlib import Path
from .static_object import COLUMN_LABELS, STRING_OBJECTS, NUMERIC_OBJECTS
from .exceptions import InvalidIncomeCodeError, InvalidSourceError, InvalidInOutValueError, \
                        InvalidDateValueError, InvalidNumericValueCodeError, InvalidSerialError
from .hidden_operation import *


# from static_object import COLUMN_LABELS, STRING_OBJECTS, NUMERIC_OBJECTS
# from exceptions import InvalidIncomeCodeError, InvalidSourceError, InvalidInOutValueError, \
#                         InvalidDateValueError, InvalidNumericValueCodeError, InvalidSerialError
# from hidden_operation import *


class BudgetAccount:
    """
    - This class is created an object based on pandas library and excel file downloaded from https://stats-admin.customs.gov.kh/
        So, in order to make this class work properly, pandas library have to be installed.
    - file_path: is path to xlsx file.
    """
    GDCE_INCOME_CODES = [
        'VPP', 'VOP', 'VAP', 'SPP', 'SOP', 'COP', 'OSF', 'DSF', 'TRF', 'TFT', 'TFF', 'TFN', 'TFB', 'TFS', 'TFP', 'TFA', 
        'OFS', 'CPP', 'ATP', 'AUC', 'PIM', 'CRP', 'ETW', 'ETR', 'ETP', 'ETO', 'PEX', 'SOS', 'VVF', 'CSF', 'STF', 'TSF', 
        'CCS', 'SOM', 'SOV', 'SOD', 'SOE', 'SOO', 'CBF', 'CDF', 'CDL', 'CDO', 'CDT', 'CPF', 'PFC', 'PFL', 'PFN', 'PFF', 
        'PFP', 'TID', 'VAF', 'ARF', 'OOD', 'CII', 'CIO', 'NII', 'NIO', 'CEF', 'OTF', 'TRF', 'TFT', 'TFF', 'TFN', 'TFB', 
        'TFS', 'TFP', 'TFA', 'TSL', 'BTL', 'TSM', 'BWM', 'CBL', 'ROL', 'ROB', 'ROO', 'SCF', 'SFS', 'SFL', 'ORB'
    ]
    def __init__(self, file_path: str):
        self.df = pd.read_excel(file_path)
        self.df["Receipt Date"] = pd.to_datetime(self.df["Receipt Date"], format="%Y-%m-%d")
        self.column_label = self.df.columns.to_list()
        

    def __available_income_codes(self):
        """
        Returns the unique budget codes from the DataFrame.

        Returns:
            numpy.ndarray: An array containing the unique budget codes.
        """
        return self.df["Budget Code"].unique()


    def get_data(self):
        """
        Return:
            - DataFrame: DataFrame of the object.
        """
        return self.df   


    def get_total_amount(self, income_code: str):
        """
        Args:
            - income_code (str): income code in GDCE Report Balance or other report patterns.
        Return:
            - int: total amount of specified income.
        """
        return self.df[self.df["Budget Code"] == income_code.upper()]["Amount"].sum()


    def get_total_amount_by_source(self, income_code: str, source: str = None):
        """
            Args:
                - income_code (str): income code in GDCE Report Balance or other report patterns.
                - sources: ASYCUDA (ASW) ans E-Customs (ECS).
            Return:
                - Return: Total amount of income in each source.
        """

        if source is not None and source.upper() not in ["ASW", "ECS"]:
            raise InvalidSourceError(f"Invalid Source {source}, Valid Source: ASW, ECS")
        if income_code not in self.__available_income_codes():
            raise InvalidIncomeCodeError(f"Invalid income code: {income_code}. Available income codes are: {self.__available_income_codes()}")

        if "source" not in self.df.columns or "Budget Code" not in self.df.columns or "Amount" not in self.df.columns:
            raise KeyError("One or more required columns are missing from the DataFrame")

        source_dataframe = self.df if source is None else self.df[self.df["source"] == source.upper().strip()]
        income_dataframe = source_dataframe["Budget Code"] == income_code.upper().strip()
    
        return source_dataframe[income_dataframe]["Amount"].sum()


    def get_return_amount(self, income_code: str):
        """
        Args: income_code (str): income code in GDCE Report Balance or other report patterns.
        return: Total amount of income returned in the dataframe.
        """
        if income_code not in self.__available_income_codes():
            raise InvalidIncomeCodeError(f"Invalid income code: {income_code}. Available income codes are: {self.__available_income_codes()}")
        
        filter_df = self.df[self.df["in_out"] == "O"]
        return filter_df[filter_df["Budget Code"] == income_code.upper()]["Amount"].sum()

    
    def get_return_amount_by_date(self, income_code: str, in_or_out: str, date_val=None):
        if in_or_out.upper() not in ["I", "O"]:
            raise InvalidInOutValueError(f"Invalid in_or_out value: {in_or_out}. Valid values are I and O.")
        if not isinstance(date_val, datetime.datetime):
            raise InvalidDateValueError(f"Invalid date value: {date_val}. Date value should be in datetime.datetime object.")
        if income_code.upper() not in self.GDCE_INCOME_CODES:
            raise InvalidIncomeCodeError(f"Invalid income code: {income_code}. Available income codes are: {self.GDCE_INCOME_CODES}")
        
        return self.df[(self.df["Receipt Date"] == date_val) & \
                (self.df["in_out"] == in_or_out.upper()) & \
                (self.df["Budget Code"] == income_code.upper())]["Amount"].sum()


class SADDetail:
    """
    - This class is created an object based on pandas library and excel file in .xlsx format from https://stats-admin.customs.gov.kh/
    - You can calculate total amount of value in each column label from the object.
    """

    IM_GROUP_ID_FILL_VALUE = 52
    EX_GROUP_ID_FILL_VALUE = 29

    STAMP_DATA = Stamp()
    STAMP_DATA_DF = STAMP_DATA.get_dataframe()
    GROUP_DATA = GroupID()
    IM_GROUP_DF = GROUP_DATA.get_IM_dataframe()
    EX_GROUP_DF = GROUP_DATA.get_EX_dataframe()

    TRANSACTION_MAP = {
                    "IM": ["I", "SI", "D"],
                    "EX": ["E", "SE"],
                    }
    def __init__(self, file_path: str):
        assert (
            Path(file_path).suffix.lower() == ".xlsx"
        ), f"Invalid file extension: {Path(file_path).suffix}"
        self.df = pd.read_excel(
            file_path, dtype={COLUMN_LABELS[key]: str for key in STRING_OBJECTS}
        )

        self.__convert_to_datetime()

        # The problem is here.
        self.dataframe = (self.df
                  .merge(self.IM_GROUP_DF, how="left", left_on=COLUMN_LABELS["hs_code"], right_on="Commodity Code")
                  .merge(self.EX_GROUP_DF, how="left", left_on=COLUMN_LABELS["hs_code"], right_on="Commodity Code")
                  .merge(self.STAMP_DATA_DF, how="left", left_on=COLUMN_LABELS["hs_code"], right_on="hs_code"))
        # print(self.STAMP_DATA_DF)   

        # Rename columns
        self.dataframe.rename(columns={'group_id_x': 'IM_group_id', 'group_id_y': 'EX_group_id'}, inplace=True)
        # Delete columns
        self.dataframe.drop(columns=['transaction_x', 'transaction_y'], inplace=True)

        # Fill empty cells in 'IM_group_id' with 52
        self.dataframe['IM_group_id'] = self.dataframe['IM_group_id'].fillna(self.IM_GROUP_ID_FILL_VALUE)

        # Fill empty cells in 'EX_group_id' with 29
        self.dataframe['EX_group_id'] = self.dataframe['EX_group_id'].fillna(self.EX_GROUP_ID_FILL_VALUE)
                  

    def __convert_to_datetime(self):
        """
        Converts specific columns in the DataFrame to datetime format.
        The columns are converted using the format "%Y-%m-%d".
        """
        date_columns = [COLUMN_LABELS["reg_date"], COLUMN_LABELS["receipt_date"]]
        for col in date_columns:
            self.df[col] = pd.to_datetime(self.df[col], format="%Y-%m-%d")


    def get_data(self):
        """
        Return:
            - DataFrame: DataFrame of the object.
        """
        return self.dataframe

    def get_data_by_group_id(self, group_id: int, transaction: str):
        """
            - This function is usef for TEST getting data (SAD) filtered by group_id.
        """
        
        list_transaction_map = list(self.TRANSACTION_MAP.keys())
        
        if transaction.upper() not in list_transaction_map:
            raise KeyError(
                f"Invalid transaction key: {transaction}. Two valid transaction keys: IM, EX (Any uppercase or lowercase)"
            )

        dataframe_by_group_id = self.dataframe[
                self.dataframe[f"{transaction.upper()}_group_id"].isin([int(group_id)])
            & 
                self.dataframe[COLUMN_LABELS["reg_serial"]].isin(self.TRANSACTION_MAP[transaction.upper()])
            & (
                self.dataframe[COLUMN_LABELS["national_procedure"]].isin(["", " ", "000"]) 
            |
                self.dataframe[COLUMN_LABELS["national_procedure"]].isnull()
            )
        ]
        print(self.TRANSACTION_MAP[transaction.upper()])
        return dataframe_by_group_id


    def get_value_by_serial(self, value_code: str, serial: str):
        """
        - value_code: Column label selected for performing calculation.
        - serial: Registration Serial
        - Return:
            int: Total Amount in column selected by value_code.
        """
        serial = [item.upper() for item in serial]  

        if value_code.lower() not in NUMERIC_OBJECTS:
            raise InvalidNumericValueCodeError(f"Invalid value_code: {value_code}. Valid value_code: {NUMERIC_OBJECTS}")
        if not all(s in ["I", "SI", "D", "E", "SE"] for s in serial):
            raise InvalidSerialError(f"Invalid serial: {serial}. Valid serial: I, SI, D, E, SE")

        return self.df[self.df[COLUMN_LABELS["reg_serial"]].isin(serial)][
            COLUMN_LABELS[value_code.lower()]
        ].sum()


    def get_value_SI(self, value_code):
        """
        Arg:
        - value_code (str) : Numeric Column Label
        Return:
        - numpy.float64 : Total amount of numeric column labels where Registration Serial are SI.
        """
        filter_df = self.df[self.df[COLUMN_LABELS["reg_serial"]] == "SI"][
            COLUMN_LABELS[value_code.lower()]
        ]
        return filter_df.sum()


    def get_min_serial(self, serial_key: str):
        """
        Returns the minimum registration number for a given serial type.
        Args:
            serial (str): The serial type (I, SI, D, E, or SE).
        Raises:
            AssertionError: If the provided serial type is invalid.
        Returns:
            str: The minimum registration number for the specified serial type.
        """
        valid_serial = ("I", "SI", "D", "E", "SI")
        assert serial_key.upper() in valid_serial, f"Invalid serial type: {serial_key}"

        return self.df[self.df["Reg. Serial"] == serial_key]["Reg. Number"].min()
        

    def get_max_serial(self, serial_key: str):
        """
        Returns the maximum registration number for a given serial type.
        Args:
            serial (str): The serial type (I, SI, D, E, or SE).
        Raises:
            AssertionError: If the provided serial type is invalid.
        Returns:
            str: The maximum registration number for the specified serial type.
        """
        valid_serial = ("I", "SI", "D", "E", "SI")
        assert serial_key.upper() in valid_serial, f"Invalid serial type: {serial_key}"

        return self.df[self.df["Reg. Serial"] == serial_key.upper()][
            "Reg. Number"
        ].max()


    def tax_amount_in_receipt(self, tax_code: str, serial: dict):
        """
        This function is used for calculating Amount of Tax only, not for calculating Non-Tax values.
        Args:
         - tax_code (str): tax_code available in Balance Report.
         - serial (dict): List of string ['E', 'I', 'SI', 'D']
        Return:
         - float: Total amount of tax (specified by tax_code)
        """
        try:
            _tax_mop = COLUMN_LABELS[f"{tax_code.lower()}_mop"]
            _tax_amount = COLUMN_LABELS[f"{tax_code.lower()}"]
            _serial = COLUMN_LABELS["reg_serial"]
        except:
            # raise KeyError(f"Column {tax_code} is not for Accounting Purpose.")
            valid_tax_code = [
                key
                for key in COLUMN_LABELS.keys()
                if COLUMN_LABELS[key].endswith("Amount")
            ]
            assert (
                tax_code in valid_tax_code
            ), f"Invalid tax_code: {tax_code}. tax_code should be in {valid_tax_code}"
        # Add tax amount where its MOP=1.
        filter_df = self.df[self.df[_tax_mop] == 1 & self.df[_serial].isin(serial)]
        return filter_df[_tax_amount].sum()


    def bur_tax_amount(self, tax_code: str, serial: dict):
        # Should update to check Valid Tax Code first.
        try:
            _tax_mop = COLUMN_LABELS[f"{tax_code.lower()}_mop"]
            _tax_amount = COLUMN_LABELS[f"{tax_code.lower()}"]
            _serial = COLUMN_LABELS["reg_serial"]
        except:
            # raise KeyError(f"Column {tax_code} is not for Accounting Purpose.")
            valid_tax_code = [
                key
                for key in COLUMN_LABELS.keys()
                if COLUMN_LABELS[key].endswith("Amount")
            ]
            assert (
                tax_code in valid_tax_code
            ), f"Invalid tax_code: {tax_code}. tax_code should be in {valid_tax_code}"

        filter_df = self.df[self.df[_tax_mop] != 1 & self.df[_serial].isin(serial)]
        return filter_df[_tax_amount].sum()


    def other_bur_tax_amount(self):
        filter_df = self.df[
            self.df[COLUMN_LABELS["national_procedure"]].isin(["007", "032", "033"])
        ]
        return filter_df[COLUMN_LABELS["bur"]].sum()


    def get_value_by_group_id(self, value_code: str, group_id: int, transaction: str):
        """
        Args:
         - value_code (str): Column name where we want to calculate
         - group_id (int): For import, rangge from 1-52 and export, range from 1-29.
         - transaction (dict): Valid transaction are 'I' (1 - 52) and 'E' (1 - 29)
        Raises:
         - KeyError: If value_code is not a numeric column.
         - KeyError: If trasaction key is not I or E.
        Return:
         - float: Total value in column for GroupType (Import or Export) that specified by value_code.
        """
        if value_code not in NUMERIC_OBJECTS:
            raise KeyError(
                f"Invalid conlumn: {value_code}. Valid value_code: {[item for item in NUMERIC_OBJECTS]}"
            )
        
        if transaction.upper() not in list(self.TRANSACTION_MAP.keys()):
            raise KeyError(
                f"Invalid transaction key: {transaction}. Two valid transaction keys: IM, EX (Any uppercase or lowercase)"
            )

        filter_df = self.dataframe[
                self.dataframe[f"{transaction.upper()}_group_id"].isin([int(group_id)])
            & 
                self.dataframe[COLUMN_LABELS["reg_serial"]].isin(self.TRANSACTION_MAP[transaction.upper()])
            & (
                self.dataframe[COLUMN_LABELS["national_procedure"]].isin(["", " ", "000"]) 
            |
                self.dataframe[COLUMN_LABELS["national_procedure"]].isnull()
            )
        ]
        return filter_df[COLUMN_LABELS[value_code.lower()]].sum()

    
    def get_value_by_only_group_id(self, value_code: list, group_id: list, Import: bool = True, Export: bool = False):
        """
        This function is updated from get_value_by_group_id function.
        Args: 
            - value_code (list): List of column name where we want to calculate.
            - group_id (int): For import, rangge from 1-52 and export, range from 1-29.
        Return: Total value in column for GroupType (Import or Export) that specified by value_code.
        """
        if any(code not in NUMERIC_OBJECTS for code in value_code):
            raise KeyError(
                f"Invalid conlumn: {value_code}. Valid value_code: {[item for item in NUMERIC_OBJECTS]}"
            )
        pass
        


    def check_available_IM_group_id(self):
        """
        Return:
            - List of available IM_group_id in the dataframe.
        """
        data_filtered = self.dataframe[self.dataframe[COLUMN_LABELS['reg_serial']].isin(self.TRANSACTION_MAP['IM'])]
        return sorted(int(i) for i in data_filtered['IM_group_id'].unique())
    
    
    def check_available_EX_group_id(self):
        """
        Return:
            - List of available EX_group_id in the dataframe.
        """
        data_filtered = self.dataframe[self.dataframe[COLUMN_LABELS['reg_serial']].isin(self.TRANSACTION_MAP['EX'])]
        return sorted(int(i) for i in data_filtered['EX_group_id'].unique())
    

    def total_number_of_stamp_used(self):
        """
        Args:
         -
        Return:
         - Total number of stamp used.
        """
        stamp_list = Stamp()
        stamp_df = stamp_list.get_dataframe()
        available_stamp = stamp_list.available_stamp()

        self.df = self.df.merge(
            stamp_df, how="left", left_on=COLUMN_LABELS["hs_code"], right_on="hs_code"
        )
        stamp_used_kind = [
            kind for kind in self.df["stamp_kind"].unique() if pd.notna(kind)
        ]
        filter_for_stamp = self.df[self.df["stamp_kind"].isin(stamp_used_kind)]

        return filter_for_stamp[COLUMN_LABELS["package"]].sum()


    def type_of_stamp_used(self):
        """
        return np.nparray: List of stamp used in the dataframe in short description
        """
        stamp_used = self.dataframe['short_description'].dropna().unique()
        return sorted(stamp_used)


    def check_availble_stamp_in_STAMP_DATA(self):
        """
        return: List of available stamp in sort description.
        """
        return sorted(self.STAMP_DATA_DF['short_description'].unique())
    
    
    def stamp_used_by_short_description(self, short_description: str):
        """
        Args:
         - stamp_description (str): Stamp Description in short
        Return:
         - Total number of stamp used by description.
        """
        data_filter = self.dataframe[self.dataframe['short_description'] == short_description.lower()]
        return data_filter[COLUMN_LABELS['package']].sum()