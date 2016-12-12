#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: make_up_missing_variables
# @Date: 2016-12-10
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import datetime

import pandas as pd
import numpy as np
import pathos
from pandas.lib import infer_dtype

from constants import dep_other_vars

today_str = datetime.datetime.today().strftime('%Y%m%d')

# define path info
root_path = '/home/wangzg/Documents/WangYouan/research/Glassdoor'
data_path = os.path.join(root_path, '20121210data')
origin_data_path = os.path.join(root_path, '20161119new_dep_var')
result_path = os.path.join(root_path, 'stata_result')
temp_path = os.path.join(root_path, '{}_temp'.format(today_str))
if not os.path.isdir(temp_path):
    os.makedirs(temp_path)


def is_simeple_num(key):
    """Check if variables end with simple or num"""
    return key.endswith('simple') or key.endswith('simple1k') or key.endswith('Num') or key.endswith('Num1k')


# load data files given by prof. Wang
da_df = pd.read_stata(os.path.join(data_path, 'da_commun_dropna.dta'))
dd_df = pd.read_stata(os.path.join(data_path, 'dd_commun_dropna.dta'))

# delete useless key
da_keys = da_df.keys()
for key in da_keys:
    if key not in dep_other_vars and not is_simeple_num(key):
        del da_df[key]

dd_keys = dd_df.keys()
for key in dd_keys:
    if key not in dep_other_vars and not is_simeple_num(key):
        del dd_df[key]

dd_df.to_pickle(os.path.join(temp_path, 'dd_commun_dropna_simple.p'))
da_df.to_pickle(os.path.join(temp_path, 'da_commun_dropna_simple.p'))

# load original data file
da_origin_df = pd.read_csv(os.path.join(origin_data_path, 'da_commun.csv'),
                           dtype={'fyear': str, 'gvkey': str, 'sic2': str})

dd_origin_df = pd.read_csv(os.path.join(origin_data_path, 'dd_commun.csv'),
                           dtype={'fyear': str, 'gvkey': str, 'sic2': str})

# delete useless key
da_keys = da_origin_df.keys()

for key in da_keys:
    if key not in dep_other_vars and not is_simeple_num(key):
        del da_origin_df[key]

dd_keys = dd_origin_df.keys()

for key in dd_keys:
    if key not in dep_other_vars and not is_simeple_num(key):
        del dd_origin_df[key]

dd_origin_df.to_pickle(os.path.join(temp_path, 'dd_commun_simple.p'))
da_origin_df.to_pickle(os.path.join(temp_path, 'da_commun_simple.p'))

da_merged = da_origin_df.merge(da_df, on=['fyear', 'gvkey'], how='outer', suffixes=['', '_dropna'])

key_set = da_merged.keys()

for key in key_set:
    if key.endswith('_dropna'):
        continue

    elif not '{}_dropna'.format(key) in key_set:
        continue

    da_merged[key] = da_merged[key].fillna(da_merged['{}_dropna'.format(key)])
    del da_merged['{}_dropna'.format(key)]

dd_merged = dd_origin_df.merge(dd_df, on=['fyear', 'gvkey'], how='outer', suffixes=['', '_dropna'])

key_set = dd_merged.keys()

for key in key_set:
    if key.endswith('_dropna'):
        continue

    elif not '{}_dropna'.format(key) in key_set:
        continue

    dd_merged[key] = dd_merged[key].fillna(dd_merged['{}_dropna'.format(key)])
    del dd_merged['{}_dropna'.format(key)]

da_merged.to_pickle(os.path.join(temp_path, 'da_merged_df.p'))
dd_merged.to_pickle(os.path.join(temp_path, 'dd_merged_df.p'))

da_merged = da_merged.sort_values('fyear')
dd_merged = dd_merged.sort_values('fyear')

process_num = 10

pool = pathos.multiprocessing.ProcessingPool(process_num)


def fill_df_missed_value(df, process_num=10):
    groups = df.groupby('gvkey')
    split_groups = np.array_split(groups, process_num)

    def process_df(group):
        new_dfs = []
        for gv_key, tmp_df in group:
            new_df = tmp_df.copy()
            ind_vars = list(set(df.keys()).difference(dep_other_vars))
            new_df[ind_vars] = new_df[ind_vars].fillna(axis=0, method='ffill')
            new_dfs.append(new_df)

        return pd.concat(new_dfs, axis=0)

    result_dfs = pool.map(process_df, split_groups)
    result_df = pd.concat(result_dfs, axis=0, ignore_index=True).reset_index(drop=True)

    # pool.close()
    return result_df


dd_fillna_merged = fill_df_missed_value(dd_merged)
da_fillna_merged = fill_df_missed_value(da_merged)

pool.close()

# drop None variables
dd_ind_vars = list(set(dd_fillna_merged.keys()).difference(dep_other_vars))
da_ind_vars = list(set(da_fillna_merged.keys()).difference(dep_other_vars))
dd_fillna_merged = dd_fillna_merged.dropna(subset=dd_ind_vars, how='all')
da_fillna_merged = da_fillna_merged.dropna(subset=da_ind_vars, how='all')

dd_fillna_merged.to_pickle(os.path.join(temp_path, 'dd_fillna_merged.p'))
da_fillna_merged.to_pickle(os.path.join(temp_path, 'da_fillna_merged.p'))

if os.path.isdir(result_path):
    os.makedirs(result_path)
dd_fillna_merged.to_stata(os.path.join(result_path, '{}_dd_fillna.dta'.format(today_str)), write_index=False)
da_fillna_merged.to_stata(os.path.join(result_path, '{}_da_fillna.dta'.format(today_str)), write_index=False)

keys = dd_fillna_merged.keys()

for key in keys:
    inferred_dtype = infer_dtype(dd_fillna_merged[key].dropna())
    if not (inferred_dtype in ('string', 'unicode') or
                    len(dd_fillna_merged[key]) == 0):
        print key
