import re
import os
import pandas


CONTENT = os.listdir("files")

FILE_CONTENT = pandas.read_excel("files/%s"%CONTENT[0], sheet_name=None, skiprows=2)

SHEETS_LIST = []
for n in range(len(FILE_CONTENT.keys()) - 1):
    SHEETS_LIST.append(n)
SHEETS_LIST.pop(0)

FILE_CONTENT = pandas.read_excel("files/%s"%CONTENT[1], sheet_name=1, skiprows=2)

DF = FILE_CONTENT
DF = DF.drop(0)
DF = DF.drop(1)
DF = DF.drop(2)


for i in range(4, len(FILE_CONTENT.index)):
    DF = DF.drop(i)
DF = DF.reset_index()
del DF["index"]

def rename_columns(dtf):
    columns_dict = {}
    names = dtf.columns.values
    for name in names:
        new_column_name = re.sub(r'\d', '%d'%i, name)
        columns_dict[name] = new_column_name
    dtf.rename(columns=columns_dict, inplace=True)
    return dtf
        
for i in range(4, len(FILE_CONTENT.index)):
    current_df = FILE_CONTENT.iloc[[i]]
    current_df = current_df.reset_index()
    del current_df["ocid"]
    del current_df["id"]
    del current_df["index"]
    current_df = rename_columns(current_df)
    print current_df
    DF = pandas.concat([DF, current_df],  axis=1)

DF.to_csv("results.csv", encoding='utf-8')

