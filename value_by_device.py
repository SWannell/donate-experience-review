# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 12:57:02 2020

@author: SWannell
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt; plt.style.use('ggplot')
import matplotlib.ticker as mtick
import seaborn as sns

lbl = pd.read_csv('..\\cro55-prompt-test\\RawData\\old_sglbl.csv')
lbl = lbl[['Response_Date', 'Response_Value', 'Platform', 'Medium', 'OS']]
lbl.columns = ['date', 'value', 'platform', 'medium', 'os']

os_device = {'iOS': 'mobile', 'Android': 'mobile', 'WinNT': 'desktop',
             'OSX': 'desktop', 'UNIX': 'desktop', 'WinXP': 'desktop',
             'Unknown': 'unknown'}

lbl['os'] = lbl['os'].replace(os_device)
lbl = lbl[lbl['value'] <= 100]
lbl = lbl[~lbl['os'].str.contains('unknown')]

# Only reasonably sized channels
nonsmall = lbl.pivot_table(values='value', index='medium',
                           aggfunc=np.count_nonzero)
nonsmall = nonsmall[nonsmall['value'] > 100].index

lbl_nonsmall = lbl[lbl['medium'].isin(nonsmall)]

# Plot
colors = ["#158aba", "#f1b13b"]
sns.set_palette(sns.color_palette(colors))
currfmt = mtick.StrMethodFormatter('£{x:,.0f}')

fig, ax = plt.subplots(1, 1, figsize=(7, 7))
sns.violinplot(x='value', y='medium', hue='os', split=True, scale='count',
               data=lbl_nonsmall, ax=ax, cut=0)
ax.xaxis.set_major_formatter(currfmt)
ax.set_title('Gift values by channel, by device', fontsize=20)
#plt.savefig('Outputs\\2020_gift_values_by_channel_split.png')