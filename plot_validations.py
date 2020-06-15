# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 17:06:07 2020

@author: SWannell
"""

import pandas as pd
import numpy as np
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
df = df[~df['page'].str.contains('/appeal')]  # donate module validation
df = df[~df['page'].str.contains('/appeal')]  # donate module validation
df['field'] = df['field'].replace('', np.nan)
df.dropna(inplace=True)

df.to_csv('AmendedData\\FormValidations.csv')

# =============================================================================
# Personal details form
# =============================================================================

personal = df[df['page'].str.contains('personaldetails')]
personal_all = personal.drop(['page', 'date'], axis=1).groupby('field').sum()
personal_total = 6435
personal_all = personal_all / personal_total
personal_all = personal_all[~personal_all.index.str.contains('delivery')]
personal_all = personal_all[~personal_all.index.str.contains('addresses')]

order = ['form-change-amount-input', 'title', 'first-name', 'surname', 'email',
         'address_1', 'address_2', 'address_3', 'address_town',
         'address_country', 'address_postcode',
         'MC_formDonationType', 'MC_formOrganisationName', 'card_name']

mapping = {field: i for i, field in enumerate(order)}
key = personal_all.index.map(mapping)
personal_all = personal_all.iloc[key.argsort()]

# =============================================================================
# Confirm details form
# =============================================================================

confirm = df[df['page'].str.contains('confirmdetails')]
confirm_all = confirm.drop(['page', 'date'], axis=1).groupby('field').sum()
confirm_total = 2819
confirm_all = confirm_all / confirm_total
confirm_all = confirm_all[~confirm_all.index.str.contains('delivery')]
confirm_all = confirm_all[~confirm_all.index.str.contains('addresses')]

key = confirm_all.index.map(mapping)
confirm_all = confirm_all.iloc[key.argsort()]

# =============================================================================
# Plot!
# =============================================================================

figs, axs = plt.subplots(1, 2, sharey=True, figsize=(10, 5))
personal_all.plot.bar(ax=axs[0], legend=None)
axs[0].set_title('Personal details')
confirm_all.plot.bar(ax=axs[1], legend=None)
axs[1].set_title('Confirm details')
axs[0].yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
plt.suptitle('Form validation % by field', fontsize=20)
figs.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('Outputs\\ValidationByField.png')