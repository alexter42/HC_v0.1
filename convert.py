import re
import os
import pandas

CONTENT = os.listdir("files")

def rename_columns(dtf,n_row):
    columns_dict = {}
    names = dtf.columns.values
    for name in names:
        new_column_name = re.sub(r'\d', '%d'%n_row, name)
        columns_dict[name] = new_column_name
    dtf.rename(columns=columns_dict, inplace=True)
    return dtf

for x, f in enumerate(CONTENT):
    FILE_CONTENT = pandas.read_excel("files/%s"%f, sheet_name=None, skiprows=2)

    SHEETS_LIST = []

    for n in range(len(FILE_CONTENT.keys()) - 1):
        SHEETS_LIST.append(n)
    SHEETS_LIST.pop(0)

    DF = pandas.DataFrame()

    for i, e in enumerate(SHEETS_LIST):
        FILE_CONTENT = pandas.read_excel("files/%s"%f, sheet_name=e, skiprows=2)
        if DF.empty:
            DF = FILE_CONTENT
            for i_row in range(3) + range(4, len(FILE_CONTENT.index)):
                DF = DF.drop(i_row)
            DF = DF.reset_index()
            del DF["index"]
        for i_row in range(4, len(FILE_CONTENT.index)):
            current_df = FILE_CONTENT.iloc[[i_row]]
            current_df = current_df.reset_index()
            try:
                del current_df["ocid"]
                del current_df["id"]
                del current_df["index"]
            except KeyError: pass
            current_df = rename_columns(current_df,i_row)
            DF = pandas.concat([DF, current_df], axis=1)

    DF.to_csv("results/%s.csv"%f.split(".", 1)[0], mode="w", encoding='utf-8')
