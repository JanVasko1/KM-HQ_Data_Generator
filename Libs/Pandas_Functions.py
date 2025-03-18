# Import Libraries
from pandas import DataFrame, Series, to_datetime, concat

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

def Dataframe_Filter_on_Multiple(Filter_df: DataFrame, Filter_Column: str, Filter_Values: list) -> DataFrame:
    filtered_df = Filter_df[Filter_df[f"{Filter_Column}"].isin(Filter_Values)]
    return filtered_df

def DataFrame_Get_One_Value(Search_df: DataFrame, Search_Column: str, Filter_Column: str, Filter_Value: str)-> str:
    filtered_values = Search_df.loc[Search_df[Filter_Column] == Filter_Value, Search_Column]
    try:
        Value = str(filtered_values.values[0])
    except:
        Value = "False"
    return Value

def Dataframe_Set_Value_on_Condition(Set_df: DataFrame, conditions: list, Set_Column: str, Set_Value: int|str|bool) -> DataFrame:
    combined_condition = conditions[0]
    for condition in conditions[1:]:
        combined_condition &= condition
    Set_df.loc[combined_condition, Set_Column] = Set_Value
    return Set_df

def Dataframe_Apply_Value_from_df2(row: Series, Fill_Column: str, Compare_Column_df1: list, Compare_Column_df2: list, Search_df: DataFrame, Search_Column: str):
    conditions = [Search_df[Compare_Column_df2[index]] == row[Compare_Column_df1[index]] for index, value in enumerate(Compare_Column_df1)]
    combined_condition = Series([True] * len(Search_df))
    for condition in conditions:
        combined_condition &= condition
    new_val = Search_df.loc[combined_condition, f"{Search_Column}"].values
    if len(new_val) > 0:
        return new_val[0]
    else:
        return row[f"{Fill_Column}"]
    
def Dataframe_Insert_Row_at_position(Insert_DataFrame: DataFrame, Insert_At_index: int, New_Row: dict):
    # Insert the new row
    df1 = Insert_DataFrame.iloc[:Insert_At_index]
    df2 = Insert_DataFrame.iloc[Insert_At_index:]
    new_df = concat([df1, DataFrame([New_Row]), df2]).reset_index(drop=True)
    return new_df

def Dataframe_Insert_Row_at_End(Insert_DataFrame: DataFrame, New_Row: dict|list):
    # Insert the new row
    Insert_DataFrame.loc[len(Insert_DataFrame)] = New_Row
    return Insert_DataFrame