#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: constants
# @Date: 2017-01-25
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import datetime

import numpy as np

portfolio_num_range = range(5, 20)
portfolio_num_range.extend(range(25, 101, 5))

holding_days_list = range(2, 15)

stop_loss_rate_range = np.arange(-0.05, 0, 0.01)

transaction_cost_list = [0.005, 0.01]
transaction_cost = 0.002

info_type_list = ['all', 'company', 'exe', 'exe_brothers', 'exe_parents', 'exe_self', 'exe_spouse']


class Constant(object):
    # trading market type
    SHANGHAI_A = 1
    SHANGHAI_B = 2
    SHENZHEN_A = 4
    SHENZHEN_B = 8
    GEM = 16  # Growth Enterprises Market Board

    working_days = 251
    initial_wealth = 10000.0

    # Other information
    ALL = 'all'
    OVERWEIGHT = u'增持'
    REDUCTION = u'减持'
    SENIOR = u'高管'
    COMPANY = u'公司'
    DIRECTOR = u'董事'
    PERSON = u'个人'
    SUPERVISOR = u'监事'

    SPOUSE = u'配偶'
    SELF = u'本人'
    PARENTS = u'父母'
    FATHER = u'父亲'
    MOTHER = u'母亲'
    OTHERS = u'其他'
    BROTHERS = u'兄弟姐妹'
    OTHER_RELATIONS = u'其他关联'

    CONTROLLED_CORPORATION = u'受控法人'
    LISTED_COMPANY = u'上市公司'

    REPORT_TICKER = 'VAR1'
    REPORT_COMPANY_NAME = 'VAR2'
    REPORT_ANNOUNCE_DATE = 'anndate'
    REPORT_ACTION = 'VAR10'
    REPORT_RELATIONSHIP = 'relation'
    REPORT_TYPE = 'type'
    REPORT_CHANGER_NAME = 'name'
    REPORT_AVERAGE_PRICE = 'average_price'
    REPORT_REASON = 'reason'
    REPORT_POSITION = 'position'
    REPORT_CHANGE_NUMBER = 'number'

    REPORT_SELL_DATE = 'sell_date'
    REPORT_RETURN_RATE = 'return'
    REPORT_BUY_DATE = 'buy_date'
    REPORT_MARKET_TICKER = 'market_ticker'
    REPORT_MARKET_TYPE = 'market_type'
    REPORT_BUY_PRICE = 'buy_price'
    REPORT_BUY_TYPE = 'buy_type'
    REPORT_SELL_TYPE = 'sell_type'

    STOCK_TICKER = 'Stkcd'
    STOCK_DATE = 'Trddt'
    STOCK_OPEN_PRICE = 'Opnprc'
    STOCK_OPEN_PRICE2 = 'Opnprc2'
    STOCK_HIGH_PRICE = 'Hiprc'
    STOCK_LOW_PRICE = 'Loprc'
    STOCK_CLOSE_PRICE = 'Clsprc'
    STOCK_CLOSE_PRICE2 = 'Clsprc2'
    STOCK_VOLUME = 'Dnshrtrd'
    STOCK_MARKET_TYPE = 'Markettype'
    STOCK_ADJPRCWD = 'Adjprcwd'
    STOCK_ADJPRCND = 'Adjprcnd'

    HOLDING_DAYS = 'holding_days'
    PORTFOLIO_NUM = 'portfolio_num'
    STOPLOSS_RATE = 'stoploss_rate'
    INFO_TYPE = 'info_type'
    TRANSACTION_COST = 'transaction_cost'
    REPORT_RETURN_PATH = 'report_return_path'
    WEALTH_DATA_PATH = 'wealth_data_path'

    WEALTH_DATAFRAME = 'raw_strategy_df'
    RETURN_DATAFRAME = 'return_df'

    REPORT_PATH = 'report path'
    TRADING_SIGNAL_PATH = 'trading signal path'

    # report between this period would be neglected
    neglect_period = [datetime.datetime(2015, 7, 8), datetime.datetime(2016, 2, 1)]

    PORTFOLIO_NUM_RANGE = portfolio_num_range
    HOLDING_DAYS_LIST = holding_days_list
    INFO_TYPE_LIST = info_type_list

    SAVE_TYPE_PICKLE = 'pickle'
    SAVE_TYPE_EXCEL = 'excel'
    SAVE_TYPE_CSV = 'csv'

    ALPHA_STRATEGY_LEGENDS = ['Raw Strategy', 'Beta Strategy', 'Alpha Strategy']

    BEST_RAW_SHARPE_RATIO = 'best_raw_sharpe_ratio'
    BEST_RAW_ANNUALIZED_RETURN = 'best_raw_ann_return'
    VALUE = 'value'
    PICTURE_PATH = 'pic_path'
    BEST_ALPHA_RETURN = 'best_alpha_return'
    BEST_ALPHA_SHARPE = 'best_alpha_sharpe'

    SHARPE_RATIO = 'sharpe_ratio'
    ANNUALIZED_RETURN = 'ann_return'
    RETURN = 'return'

    RAW_STRATEGY = 'raw'
    ALPHA_STRATEGY = 'alpha'
    BETA_STRATEGY = 'beta'