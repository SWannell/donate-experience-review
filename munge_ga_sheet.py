# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 11:48:38 2020

@author: SWannell
"""

import pandas as pd
import pickle

fp = r'RawData\\2020 06 DXR_form validation.xlsx'
ref_str = 'FormValidation'

xls = pd.ExcelFile(fp)
sheets = xls.sheet_names
sheets = sheets[1:-1]

df_dict = dict([])
for sheet in sheets:
    df = pd.read_excel(xls, sheet, skiprows=14)
    df.drop(list(df.filter(regex='Unnamed')), axis=1, inplace=True)
    sheet_key = sheet.replace(ref_str, '')
    sheet_date = pd.to_datetime('2020'+sheet_key)
    df['date'] = sheet_date
    df_dict[sheet_key] = df

with open('AmendedData\\dfdict{}.pickle'.format(ref_str), 'wb') as handle:
    pickle.dump(df_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)