# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 11:48:38 2020

@author: SWannell
"""

import pandas as pd
import pickle

fp = r'RawData\\2020 06 Form conv rates by month.xlsx'
xls = pd.ExcelFile(fp)
sheets = xls.sheet_names
sheets = sheets[1:-1]

df_dict = dict([])
for sheet in sheets:
    df = pd.read_excel(xls, sheet, skiprows=14)
    df.drop(list(df.filter(regex='Unnamed')), axis=1, inplace=True)

with open('AmendedData\\dfdict.pickle', 'wb') as handle:
    pickle.dump(df_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)