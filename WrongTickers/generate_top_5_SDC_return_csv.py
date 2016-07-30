#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: wrong_tickers_of_top5_return
# Author: Mark Wang
# Date: 30/7/2016

import pandas as pd

# get top 5% mna target return records
df = pd.read_csv('result_csv/SDC_CRSP(renamed).csv', index_col=0)
df['MnATargetReturn'] = (df['TargetClosingPrice1DayAfterAnnDate'] - df['TargetSharePrice1DayPriortoAnnouncement']) / \
                        df['TargetSharePrice1DayPriortoAnnouncement']

df = df.sort_values('MnATargetReturn', ascending=False).head(int(0.05 * df.shape[0]) + 1)
df.reset_index(drop=True).to_csv('result_csv/SDC_CRSP_rename_top5pc.csv', encoding='utf8')
del df
