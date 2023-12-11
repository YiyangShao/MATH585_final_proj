#region imports
from AlgorithmImports import *
import numpy as np
import openai
import pandas as pd
from gpt_prompt import get_sentiment_general, get_sentiment_general_parallel, get_sentiment_general_sequence
import time
from io import StringIO
from datetime import timedelta
#endregion



# https://www.quantconnect.com/terminal/processCache?request=embedded_backtest_86c13c3d961b8009d7f767e12e857a0b.html

class TiingoNewsDataAlgorithm(QCAlgorithm):

    def __init__(self):
        self.alpha1 = 0.2
        self.alpha2 = 0.2
        self.alpha3 = -0.2
        self.holding_time1 = 20
        self.holding_time2 = 60
        self.holding_time3 = 60
        self.long_thres = 1
        self.short_thres = -1

    def Initialize(self) -> None:
        self.start_date = datetime(2023, 1, 1)
        self.end_date = datetime(2023, 12, 1)
        
        self.SetStartDate(self.start_date)
        self.SetEndDate(self.end_date)
        self.SetCash(1000000)
        
        self.current_holdings = 0
        self.target_holdings = 0
        self.sample_size = 50
        self.SetWarmup(-1)

        self.timer1 = []
        self.timer2 = []
        self.timer3 = []
        
        # Requesting data
        self.aapl = self.AddEquity("AAPL", Resolution.Minute).Symbol
        self.tiingo_symbol = self.AddData(TiingoNews, self.aapl, resolution=Resolution.Minute).Symbol

        self.num_bull = 0
        self.num_neu = 0
        self.num_bear = 0
        
        self.prev_price = 0
        self.sentiments = []

        file = self.Download("https://www.dropbox.com/scl/fi/mx7tm4z0v2nocbdu5aab7/news_score_apple_2023_all.csv?rlkey=xgettu0emvbcmpr8x3ptq71eh&dl=1")
        self.score_df = pd.read_csv(StringIO(file))

        self.score_dic = self.score_df.set_index('date')['score'].to_dict()
        
        
    def OnData(self, slice: Slice) -> None:
        cur_time = self.Time
        if self.timer1:
            to_sell1 = 0
            for t in self.timer1:
                if (cur_time - t) > timedelta(minutes=self.holding_time1):
                    to_sell1 += 1
            self.timer1 = self.timer1[to_sell1:]
            self.target_holdings -= self.alpha1 * to_sell1

        if self.timer2:
            to_sell2 = 0
            for t in self.timer2:
                if (cur_time - t) > timedelta(minutes=self.holding_time2):
                    to_sell2 += 1
            self.timer2 = self.timer2[to_sell2:]
            self.target_holdings -= self.alpha2 * to_sell2

        if self.timer3:
            to_sell3 = 0
            for t in self.timer3:
                if (cur_time - t) > timedelta(minutes=self.holding_time3):
                    to_sell3 += 1
            self.timer3 = self.timer3[to_sell3:]
            self.target_holdings -= self.alpha3 * to_sell3

        if slice.ContainsKey(self.tiingo_symbol) and self.Securities[self.aapl].Price != None:
            title_words = slice[self.tiingo_symbol].Title + slice[self.tiingo_symbol].Description
            cur_time = f"{self.Time}"[:19]
            if cur_time in self.score_dic:
                score = self.score_dic[cur_time]
                if score == 1:
                    self.target_holdings += self.alpha1
                    self.timer1.append(self.Time)
                if score == -1:
                    self.target_holdings += self.alpha2
                    self.timer2.append(self.Time)
                if score == 0:
                    self.target_holdings += self.alpha3
                    self.timer3.append(self.Time)
        
        # if self.current_holdings != self.target_holdings:
        #     self.target_holdings = round(self.target_holdings, 2)
        #     self.real_holdings = self.target_holdings
        #     if self.target_holdings > 1:
        #         self.real_holdings = 1
        #     if self.target_holdings < -1:
        #         self.real_holdings = -1
        #     self.Debug(f"{self.current_holdings} {self.target_holdings} {self.Time}")
        #     self.SetHoldings(self.aapl,  self.real_holdings)
        #     self.current_holdings = self.target_holdings


    def OnEndOfDay(self):
        if self.current_holdings != self.target_holdings:
            self.target_holdings = round(self.target_holdings, 2)
            self.real_holdings = self.target_holdings
            if self.target_holdings > 1:
                self.real_holdings = 1
            if self.target_holdings < -1:
                self.real_holdings = -1
            self.Debug(f"{self.current_holdings} {self.target_holdings} {self.Time}")
            self.SetHoldings(self.aapl,  self.real_holdings)
            self.current_holdings = self.target_holdings