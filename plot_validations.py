# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 17:06:07 2020

@author: SWannell
"""

import pandas as pd
import matplotlib.pyplot as plt; plt.style.use('ggplot')
import matplotlib.ticker as mtick
import pickle

with open('AmendedData\\dfdictFormValidation.pickle', 'rb') as handle:
    df_dict = pickle.load(handle)

df = pd.concat(df_dict.values(), sort=False)
df.reset_index(inplace=True, drop=True)
df.columns = ['page', 'field', 'events', 'date']
df['page'] = df['page'].str.replace('donate.redcross.org.uk', '')
df['field'] = df['field'].str.replace('View_', '')

personal = df[df['page'].str.contains('personaldetails')]
personal_all = personal.drop(['page', 'date'], axis=1).groupby('field').sum()
personal_total = 6435
personal_all = personal_all / personal_total
personal_all = personal_all[~personal_all.index.str.contains('delivery')]
personal_all = personal_all[~personal_all.index.str.contains('addresses')]

blocks = {0: ['form-change-amount-input'],
          1: ['title', 'first-name', 'surname', 'email'],
          2: [s for s in personal['field'].unique() if s.startswith('address_')],
          3: [s for s in personal['field'].unique() if 'MC_' in s],
          4: ['card_name']}

for i in personal_all.index:
    for k, v in blocks.items():
        if i in v:
            personal_all.loc[i, 'block'] = k

personal_all.sort_values(by='block')['events'].plot.bar()

personal_all.sort_values(by='events', ascending=False).plot.bar()