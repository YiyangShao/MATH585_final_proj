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





class TiingoNewsDataAlgorithm(QCAlgorithm):

    def __init__(self):
        self.alpha1 = 0.4
        self.alpha2 = -0.4
        self.alpha3 = 0.4
        self.holding_time1 = 60
        self.holding_time2 = 5
        self.holding_time3 = 60

    def Initialize(self) -> None:
        self.start_date = datetime(2021, 1, 4)
        self.end_date = datetime(2021, 1, 4)
        
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
            cur_time = f"{self.Time}"
            response = get_sentiment_general(title_words,company="Apple",model="gpt-3.5-turbo-1106", output="polar", explanation=False)
            dic = {"BULLISH": 1, "NEUTRAL": 0, "BEARISH":-1}
            score = dic[response[0]]
            self.Debug(f"{score} {title_words}")
            if score == 1:
                self.target_holdings += self.alpha1
                self.timer1.append(self.Time)
            if score == -1:
                self.target_holdings += self.alpha2
                self.timer2.append(self.Time)
            if score == 0:
                self.target_holdings += self.alpha3
                self.timer3.append(self.Time)
        
        if self.current_holdings != self.target_holdings:
            self.target_holdings = round(self.target_holdings, 2)
            if self.target_holdings > 1:
                self.target_holdings = 1
            if self.target_holdings < -1:
                self.target_holdings = 1
            self.Debug(f"{self.current_holdings} {self.target_holdings} {self.Time}")
            self.SetHoldings(self.aapl, self.target_holdings)
            self.current_holdings = self.target_holdings