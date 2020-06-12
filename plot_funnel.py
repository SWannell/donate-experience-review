# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 12:08:51 2020

@author: SWannell
"""

import pandas as pd
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

cvr_by_platform['paypal'].plot(legend=None)

#    print(b, c)

#for k in df_dict.keys():
#    _ = df_dict[k]
#    _ = _[['Page', 'Unique Pageviews']]
#    _.columns = ['page', '!PVs']
#    _['page'] = _['page'].str.replace('donate.redcross.org.uk/appeal/', '')
#    _ = _[_['!PVs'] > 3]
#    _.set_index('page', inplace=True)
#    df_dict[k] = _
## Check all the same
#for k in df_dict.keys():
#    print(sorted(df_dict[k].index))
#
#month_map = ['2020-0{}'.format(i) for i in [1, 2, 3]]
#appeals_viewed = sorted(df_dict[2].index)
#appealmonth = pd.MultiIndex.from_product([appeals_viewed, month_map],
#                                         names=['appeal', 'month'])
#traffic_by_month = pd.DataFrame(index=appealmonth)
#traffic_by_month['viewed'] = 0
#traffic_by_month.to_csv('AmendedData\\traffic_by_month.csv')
#
#for (k, mth) in zip(df_dict.keys(), month_map):
#    _ = df_dict[k]
#    for appeal in _.index:
#        traffic_by_month.loc[appeal, mth]['viewed'] = _.loc[appeal]['!PVs']