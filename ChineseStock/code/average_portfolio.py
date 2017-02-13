#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: average_portfolio
# @Date: 2017-01-31
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

from constants import Constant as const
from path_info import daily_date_sep_path
from portfolio import Investment


class AveragePortfolio(object):
    def __init__(self, total_num=10, total_value=10000., transaction_cost=0, price_type=const.STOCK_ADJPRCWD):

        self.free_amount = total_value
        self.free_account_num = total_num
        self.account_list = []
        self.wealth_stock_type = price_type
        self.transaction_cost = transaction_cost

    def short_stocks(self, end_date, stock_return, current_date, buy_price, stock_ticker, stock_type=None):
        """ If there is a free account, buy target stock, else do nothing """
        if self.free_account_num == 0:
            return

        buy_amount = float(self.free_amount) / self.free_account_num
        self.free_amount -= buy_amount
        account = Investment(amount=buy_amount,
                             stock_price_type=self.wealth_stock_type,
                             price_path=daily_date_sep_path,
                             transaction_cost=self.transaction_cost)
        account.short_stock(return_rate=stock_return, buy_price=buy_price, end_date=end_date, stock_type=stock_type,
                            stock_ticker=stock_ticker)
        self.account_list.append(account)
        self.free_account_num -= 1

    def get_current_values(self, current_date):
        """ get current investment value """
        amount = self.free_amount
        new_amount_list = []

        for account in self.account_list:
            amount += account.get_current_value(current_date)
            if account.is_free(current_date):
                self.free_amount += account.get_current_value(current_date)
                self.free_account_num += 1

            else:
                new_amount_list.append(account)

        self.account_list = new_amount_list

        return amount