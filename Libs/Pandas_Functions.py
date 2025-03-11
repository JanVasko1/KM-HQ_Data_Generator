# Import Libraries
from pandas import DataFrame, Series, to_datetime

# --------------------------------------------- Pandas --------------------------------------------- #
def PD_Column_to_DateTime(PD_DataFrame: DataFrame, Column: str, Covert_Format: str) -> DataFrame:
    PD_DataFrame[Column] = to_datetime(arg=PD_DataFrame[Column], format=Covert_Format)
    return PD_DataFrame

def Dataframe_sort(Sort_Dataframe: DataFrame, Columns_list: list, Accenting_list: list) -> None:
    # Sort Dataframe and reindex 
    Sort_Dataframe.sort_values(by=Columns_list, ascending=Accenting_list, axis=0, inplace = True)
    Sort_Dataframe.reset_index(inplace=True)
    Sort_Dataframe.drop(labels=["index"], inplace=True, axis=1)
    return Sort_Dataframe

def Dataframe_Apply_Value(row: Series, Fill_Column: str, Compare_Column_df1: list, Compare_Column_df2: list, Search_df: DataFrame, Search_Column: str):
    conditions = [Search_df[Compare_Column_df2[index]] == row[Compare_Column_df1[index]] for index, value in enumerate(Compare_Column_df1)]
    combined_condition = Series([True] * len(Search_df))
    for condition in conditions:
        combined_condition &= condition
    new_val = Search_df.loc[combined_condition, f"{Search_Column}"].values
    if len(new_val) > 0:
        return new_val[0]
    else:
        return row[f"{Fill_Column}"]