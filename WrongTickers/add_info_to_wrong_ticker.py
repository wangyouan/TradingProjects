#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: add_info_to_wrong_ticker
# Author: Mark Wang
# Date: 16/8/2016

import os
import datetime

import pandas as pd
import numpy as np

data_path = 'Stock_data'


def get_information_from_saved_file(row_info, ticker_type='wrong', info_type='volume', date_type='Today'):
    if date_type == 'Today':
        date = row_info['DateToday']
    elif date_type == 'Tomorrow':
        date = row_info['DateTomorrow']
    else:
        date = row_info['DateYesterday']

    date = ''.join(date.split('-'))
    if ticker_type.lower() == 'wrong':
        ticker = row_info['WrongTicker']
    else:
        ticker = row_info['Ticker']
    try:
        if info_type.lower() == 'volume':
            path = os.path.join('Stock_data', 'volume', '{}_VOL.csv'.format(ticker))
            if not os.path.isfile(path):
                return np.nan
            df = pd.read_csv(path, usecols=['date', 'VOL'], dtype={'date': str, 'VOL': float})
            df = df[df['date'] == date]
            if df.empty:
                return np.nan
            else:
                if not np.isnan(df.ix[df.index[0], 'VOL']):
                    return int(df.ix[df.index[0], 'VOL'])
                else:
                    return np.nan

        elif info_type.lower() == 'Price'.lower():
            path = os.path.join('Stock_data', 'Price', '{}_PRC.csv'.format(ticker))
            if not os.path.isfile(path):
                return np.nan
            df = pd.read_csv(path, usecols=['date', 'PRC'], dtype={'date': str, 'PRC': float})
            df = df[df['date'] == date]
            if df.empty:
                return np.nan
            else:
                return df.ix[df.index[0], 'PRC']

        elif info_type.lower() == 'LogReturn'.lower():
            path = os.path.join('Stock_data', 'logReturn', '{}_LR.csv'.format(ticker))
            if not os.path.isfile(path):
                return np.nan
            df = pd.read_csv(path, header=None, names=['date', 'LR'])
            df['date'] = df['date'].apply(lambda x: ''.join(x.split('-')))
            df = df[df['date'] == date]
            if df.empty:
                return np.nan
            else:
                return df.ix[df.index[0], 'LR']

        elif info_type.lower() == 'SimpleReturn'.lower():
            path = os.path.join('Stock_data', 'simpleReturn', '{}_SR.csv'.format(ticker))
            if not os.path.isfile(path):
                return np.nan
            df = pd.read_csv(path, header=None, names=['date', 'SR'])
            df['date'] = df['date'].apply(lambda x: ''.join(x.split('-')))
            df = df[df['date'] == date]
            if df.empty:
                return np.nan
            else:
                return df.ix[df.index[0], 'SR']

        elif info_type.lower() == 'PriceHigh'.lower():
            path = os.path.join('Stock_data', 'highlow', '{}_HL.csv'.format(ticker))
            if not os.path.isfile(path):
                return np.nan
            df = pd.read_csv(path, usecols=['date', 'ASKHI'], dtype={'date': str, 'ASKHI': float})
            df = df[df['date'] == date]
            if df.empty:
                return np.nan
            else:
                return df.ix[df.index[0], 'ASKHI']

        elif info_type.lower() == 'PriceLow'.lower():
            path = os.path.join('Stock_data', 'highlow', '{}_HL.csv'.format(ticker))
            if not os.path.isfile(path):
                return np.nan
            df = pd.read_csv(path, usecols=['date', 'BIDLO'], dtype={'date': str, 'BIDLO': float})
            df = df[df['date'] == date]
            if df.empty:
                return np.nan
            else:
                return df.ix[df.index[0], 'BIDLO']

        else:
            return np.nan
    except Exception, err:
        raise Exception('Ticker {}, info: {}, err: {}'.format(ticker, info_type, err))


def get_wrong_ticker_information_from_saved_file(row_info, info_type='volume', date_type='Today'):
    return get_information_from_saved_file(row_info, ticker_type='wrong', info_type=info_type, date_type=date_type)


def add_wrong_ticker_price_volume_return_info(csv_path):
    target_df = pd.read_csv(csv_path, index_col=0)

    info_to_add = ['Volume', 'Price', 'LogReturn', 'SimpleReturn', 'PriceHigh', 'PriceLow']
    for info in info_to_add:
        for required_time in ['Today', 'Tomorrow', 'Yesterday']:
            if required_time == 'Today':
                column_name = info
            else:
                column_name = "{}{}".format(info, required_time)

            target_df[column_name] = target_df.apply(
                axis=1, func=lambda x: get_wrong_ticker_information_from_saved_file(x, info, required_time))

    target_df['PriceRange'] = target_df['PriceHigh'] - target_df['PriceLow']
    target_df['PriceRangeYesterday'] = target_df['PriceHighYesterday'] - target_df['PriceLowYesterday']
    target_df['PriceRangeTomorrow'] = target_df['PriceHighTomorrow'] - target_df['PriceLowTomorrow']
    target_df.to_csv(csv_path, encoding='utf8')


def rename_wrong_ticker_column(data_df):
    if 'Volume' not in data_df.keys():
        return data_df
    name_to_change = ['Volume', 'Price', 'LogReturn', 'SimpleReturn', 'PriceHigh', 'PriceLow', 'PriceRange']
    for name in name_to_change:
        tomorrow_name = "{}Tomorrow".format(name)
        yesterday_name = "{}Yesterday".format(name)
        data_df["{}_wrong".format(name)] = data_df[name]
        data_df["{}_wrong".format(tomorrow_name)] = data_df[tomorrow_name]
        data_df["{}_wrong".format(yesterday_name)] = data_df[yesterday_name]
        del data_df[name]
        del data_df[tomorrow_name]
        del data_df[yesterday_name]
    return data_df


def add_real_price_stock_info(data_path, df_type='SDC'):
    data_df = pd.read_csv(data_path, index_col=0)
    # this used for add real info to dataframe
    if df_type != 'SDC':
        print 'Load Bloomberg file info'
        reference_df = pd.read_csv('result_csv/Bloomberg_CRSP_rename_top5pc.csv', index_col=0)
        company_name = 'Company Name'
        data_column = 'DateToday'
    else:
        print 'Load SDC file info'
        reference_df = pd.read_csv('result_csv/SDC_CRSP_rename_top5pc.csv', index_col=0)
        company_name = 'TargetName'
        data_column = '  DateAnnounced'

    keys_to_add = reference_df.keys()
    for key in keys_to_add:
        data_df.loc[:, '{}_real'.format(key)] = None

    for index in data_df.index:
        ticker = data_df.ix[index, 'Company Name']
        date_today = data_df.ix[index, 'DateToday']
        reference_info = reference_df[reference_df[company_name] == ticker][reference_df[data_column] == date_today]
        if reference_info.empty:
            print data_df.ix[index, 'Company Name'], data_df.ix[index, 'Ticker'], data_df.ix[index, 'DateToday']
            continue

        for key in keys_to_add:
            data_df.loc[index, '{}_real'.format(key)] = reference_df.ix[reference_info.index[0], key]

    data_df.to_csv(data_path, encoding='utf8')


def get_comp_df_info(cusip, date, data_type='real', date_type='Today'):
    df_path = os.path.join(data_path, 'Compustat_cusip', '{}_COMPU.csv'.format(cusip))
    if date_type.lower() == 'today':
        pad = '_{}'.format(data_type)
    else:
        pad = '{}_{}'.format(date_type, data_type)
    if not os.path.isfile(df_path):
        return {
            'gvkey{}'.format(pad): np.nan,
            'iid{}'.format(pad): np.nan,
            'divd{}'.format(pad): np.nan,
            'cshoc{}'.format(pad): np.nan,
            'eps{}'.format(pad): np.nan,
            'trfd{}'.format(pad): np.nan,
            'exchg{}'.format(pad): np.nan,
        }
    date = ''.join(date.split('-'))
    df = pd.read_csv(df_path, dtype={'cusip': str, 'iid': str, 'datadate': str})
    df = df[df['datadate'] == date]
    if df.empty:
        return {
            'gvkey{}'.format(pad): np.nan,
            'iid{}'.format(pad): np.nan,
            'divd{}'.format(pad): np.nan,
            'cshoc{}'.format(pad): np.nan,
            'eps{}'.format(pad): np.nan,
            'trfd{}'.format(pad): np.nan,
            'exchg{}'.format(pad): np.nan,
        }
    else:
        index = df.index[0]
        return {
            'gvkey{}'.format(pad): df.ix[index, 'gvkey'],
            'iid{}'.format(pad): df.ix[index, 'iid'],
            'divd{}'.format(pad): df.ix[index, 'divd'],
            'cshoc{}'.format(pad): df.ix[index, 'cshoc'],
            'eps{}'.format(pad): df.ix[index, 'eps'],
            'trfd{}'.format(pad): df.ix[index, 'trfd'],
            'exchg{}'.format(pad): df.ix[index, 'exchg'],
        }


def get_prior_one_year_volume(date, cusip):
    file_path = os.path.join(data_path, 'volume_cusip', '{}_VOL.csv'.format(cusip))
    if not os.path.isfile(file_path):
        return np.nan, np.nan
    df = pd.read_csv(file_path, usecols=['VOL', 'date'], dtype={'date': str, 'VOL': int})
    df['date'] = df['date'].apply(lambda x: datetime.datetime.strptime(x, '%Y%m%d'))
    current_date = datetime.datetime.strptime(date, '%Y-%m-%d')
    df = df[df.date < current_date].tail(252)
    if df.empty:
        return np.nan, np.nan
    else:
        return df['VOL'].sum(), df['VOL'].std
