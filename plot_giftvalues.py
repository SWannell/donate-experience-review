# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 12:24:14 2020

@author: SWannell
"""

import pandas as pd
import matplotlib.pyplot as plt; plt.style.use('ggplot')
import matplotlib.ticker as mtick

lbl = pd.read_csv('..\\cro55-prompt-test\\AmendedData\\LBL.csv')
colours = ['#1d1a1c', '#ee2a24']
lbl = lbl[['value', 'cell']]
lbl = lbl[lbl['value'] <= 100]

prompts = {'ctrl': [5, 25, 50], 'test': [10, 30, 60]}

## Histogram vs prompts
fig, ax = plt.subplots(1, 2, figsize=(10, 6), sharey=True)
bins = range(2, 100, 1)
currfmt = mtick.StrMethodFormatter('£{x:,.0f}')
for i, cell in enumerate(prompts.keys()):
    df = lbl[lbl['cell'] == cell]['value']
    df.plot.hist(color=colours[1], ax=ax[i], legend=False, bins=bins)
    ax[i].set_xlabel('Donation value')
    ax[i].xaxis.set_major_formatter(currfmt)
    for prompt_val in prompts[cell]:
        ax[i].vlines(prompt_val, 0, 50, color=colours[0], alpha=0.5)
    ax[i].set_title(cell)
plt.suptitle('CRO55 gift values vs prompts', fontsize=20)
fig.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('Outputs\\GiftValuesvsPrompts.png')

# On vs off prompt
on_prompt = 0
for cell in prompts.keys():
    df = lbl[lbl['cell'] == cell]['value']
    for prompt in prompts[cell]:
        on_val = df.value_counts().loc[prompt]
        on_prompt += on_val
off_prompt = len(lbl) - on_prompt
on_prompts = pd.DataFrame(index=['on', 'off'], columns=['count'])
on_prompts.loc['on'] = on_prompt
on_prompts.loc['off'] = off_prompt
on_prompts.plot.pie('count', colors=colours[::-1])
plt.title('% of gifts on vs off prompt\n(CRO55 prompt test)')
plt.savefig('Outputs\\GiftsOnPrompts.png')