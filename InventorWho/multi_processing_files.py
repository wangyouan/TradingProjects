#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: multi_processing_files
# @Date: 2016-12-08
# @Author: Mark Wang
# @Email: wangyouan@gmial.com


import os

import pandas as pd
import numpy as np
import pathos

root_path = '/home/zigan/Documents/WangYouan/research/InventorWho'
data_path = os.path.join(root_path, 'data')
tmp_path = os.path.join(root_path, 'temp')
inventor_data_path = os.path.join(tmp_path, 'inventor')
citation_result_path = os.path.join(root_path, 'citation_result')
patent_count_result_path = os.path.join(root_path, 'result')


def process_file(file_list):
    patent_count = pd.DataFrame(columns=['name_last', 'name_first', 'patent_num', 'fc_gt_1',
                                         'fc_gt_5', 'fc_gt_10', 'fc_gt_20', 'fc_gt_50', 'fc_gt_100', 'patent_coverage',
                                         'first_patent_year', 'first_city', 'last_city', 'last_patent_year'])

    for file_name in file_list:
        if not file_name.endswith('.p'):
            continue

        inventor_id = file_name[:-2]
        df = pd.read_pickle(os.path.join(inventor_data_path, file_name))

        result_dict = {'fc_gt_5': df[df[u'forwardCitationCountToSampleEnd'] > 5].shape[0],
                       'fc_gt_1': df[df[u'forwardCitationCountToSampleEnd'] > 1].shape[0],
                       'fc_gt_10': df[df[u'forwardCitationCountToSampleEnd'] > 10].shape[0],
                       'fc_gt_20': df[df[u'forwardCitationCountToSampleEnd'] > 20].shape[0],
                       'fc_gt_50': df[df[u'forwardCitationCountToSampleEnd'] > 50].shape[0],
                       'fc_gt_100': df[df[u'forwardCitationCountToSampleEnd'] > 100].shape[0],
                       'patent_num': df.shape[0],
                       }
        year_series = map(int, df.year.dropna().tolist())
        if len(year_series) > 0:
            year_set = set(year_series)
            result_dict['first_patent_year'] = year_series[0]
            result_dict['last_patent_year'] = year_series[-1]
            result_dict['patent_coverage'] = float(len(year_set)) / float(len(year_series))
        else:
            result_dict['first_patent_year'] = np.nan
            result_dict['last_patent_year'] = np.nan
            result_dict['patent_coverage'] = np.nan

        city_series = df.city.dropna().tolist()
        if len(city_series) > 0:
            result_dict['first_city'] = city_series[0]
            result_dict['last_city'] = city_series[-1]
        else:
            result_dict['first_city'] = np.nan
            result_dict['last_city'] = np.nan

        first_name = df.name_first.dropna().tolist()
        last_name = df.name_last.dropna().tolist()
        if first_name:
            result_dict['name_first'] = first_name[0]
        else:
            result_dict['name_first'] = np.nan
        if last_name:
            result_dict['name_last'] = last_name[0]
        else:
            result_dict['name_last'] = np.nan
        patent_count.loc[inventor_id] = result_dict

    return patent_count


if __name__ == '__main__':
    process_num = 20
    file_list = os.listdir(inventor_data_path)
    split_files = np.array_split(file_list, process_num)

    print 'init pool'
    pool = pathos.multiprocessing.ProcessingPool(process_num)

    print 'process dfs'
    result_dfs = pool.map(process_file, split_files)

    print 'save result'
    result_df = pd.concat(result_dfs, axis=0)
    result_df.index.name = 'inventor_id'
    result_df.to_pickle(os.path.join(tmp_path, 'forward_citation.p'))
    result_df.to_csv(os.path.join(patent_count_result_path, 'forward_citation.csv'))