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
months = sorted(df['month'].unique())

cvr_by_platform = {k: None for k in payment_types}

for platform in payment_types:
    by_month = pd.DataFrame(index=months)
    for appeal in bigappeal.index:
        _ = df[df['appeal'] == appeal]
        a = _[_['payment'] == platform]
        a.drop('appeal', axis=1, inplace=True)
        b = a.pivot_table(index='month', columns='formpage')
        for mth in b.index:
            first_step = b['users'].max(axis=1).loc[mth]
            ty_step = b['users'].loc[mth, 'Thank you']
            formpct = ty_step/first_step
            by_month.loc[mth, appeal] = formpct
    cvr_by_platform[platform] = by_month

figs, axs = plt.subplots(1, 3, sharey=True, figsize=(13, 5))
for i, platform in enumerate(cvr_by_platform.keys()):
    platform_data = cvr_by_platform[platform]
    # Added these bizarre steps to get it to add xticklabels
    platform_data = platform_data.reset_index()
    platform_data = platform_data.rename(columns={"index": "month"})
    platform_data.plot(legend=None, ax=axs[i], marker='o', linestyle='None',
                       xticks=platform_data.index)
    axs[i].set_xticklabels(months)
    axs[i].set_title(platform)
    axs[i].yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
plt.suptitle('Form:TY conversion rate by appeal', fontsize=20)
plt.savefig('Outputs\\CVR_from-form_payment-type.png')

landing_cvr = pd.DataFrame(index=months)
for appeal in bigappeal.index:
    steps = {'Appeal Landing': 0, 'Thank you': 0}
    for step in steps:
        data = df[(df['formpage'] == step) & (df['appeal'] == appeal)]
        data = data[['month', 'users']]
        data.set_index('month', inplace=True)
        data.columns = [appeal]
        if len(data.index) != len(data.index.unique()):
            data = data.groupby('month').sum()
        steps[step] = data
    cvr = steps['Thank you'] / steps['Appeal Landing']
    landing_cvr = landing_cvr.join(cvr)

fig, ax = plt.subplots(1, 1, figsize=(6, 6))
landing_cvr.plot(legend=None, marker='o', ax=ax, linestyle='None')
plt.xticks(range(len(landing_cvr.index)), landing_cvr.index)
ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
ax.set_title('Landing:TY conversion rate by appeal', fontsize=20)
plt.savefig('Outputs\\CVR_from-landing.png')