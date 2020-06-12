# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 12:08:51 2020

@author: SWannell
"""

import pandas as pd
import matplotlib.pyplot as plt; plt.style.use('ggplot')
import matplotlib.ticker as mtick
import pickle

with open('AmendedData\\dfdict.pickle', 'rb') as handle:
    df_dict = pickle.load(handle)

for sheet in df_dict.keys():
    [page, month] = sheet.split('_')
    df_dict[sheet]['month'] = month

df = pd.concat(df_dict.values(), sort=False)
df.reset_index(inplace=True, drop=True)

df.columns = ['formpage', 'appeal', 'payment', 'users', 'month']
df['appeal'] = df['appeal'].str.replace('Donate_', '')

bigappeal = df.groupby('appeal').sum().sort_values(by='users', ascending=False)
bigappeal = bigappeal[bigappeal['users'] > 1000]

df = df[df['appeal'].isin(bigappeal.index)]

df[['formpage', 'payment']].drop_duplicates().sort_values(by='payment')

payment_types = ['card', 'paypal', 'direct-debit']
# for appeal in bigappeal.index:
#for platform in ['card', 'paypal', 'direct-debit']:
for appeal in ['Kindness Starts With You']:
    print(df[df['appeal'] == appeal])
    appeal_df = pd.DataFrame(index=['19-12', '20-01', '20-02', '20-03',
                                    '20-04', '20-05'],
                             columns=[''])

months = sorted(df['month'].unique())

cvr_by_platform = {k: None for k in payment_types}

for platform in payment_types:
#for platform in ['card']:
    by_month = pd.DataFrame(index=months)
    for appeal in bigappeal.index:
        _ = df[df['appeal'] == appeal]
        a = _[_['payment'] == platform]
        a.drop('appeal', axis=1, inplace=True)
        b = a.pivot_table(index='month', columns='formpage')
        for mth in b.index:
            print(mth, platform)
            first_step = b['users'].max(axis=1).loc[mth]
            ty_step = b['users'].loc[mth, 'Thank you']
            formpct = ty_step/first_step
            print('{}/{} = {:.0f}%'.format(ty_step, first_step, 100*formpct))
            by_month.loc[mth, appeal] = formpct
    cvr_by_platform[platform] = by_month

fig, axs = plt.subplots(1, 3, sharey=True, figsize=(13, 5))
for i, platform in enumerate(cvr_by_platform.keys()):
    platform_data = cvr_by_platform[platform]
    # Added these bizarre steps to get it to add xticklabels
    platform_data = platform_data.reset_index()
    platform_data = platform_data.rename(columns={"index":"month"})
    platform_data.plot(legend=None, ax=axs[i], marker='o', linestyle='None', xticks=platform_data.index)
    axs[i].set_xticklabels(months)
    axs[i].set_title(platform)
    axs[i].yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
plt.suptitle('Form conversion rate by payment type', fontsize=20)
plt.savefig('Outputs\\CVR_from-form_payment-type.png')