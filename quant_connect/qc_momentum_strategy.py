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

    def Initialize(self) -> None:
        self.start_date = datetime(2022, 1, 1)
        self.end_date = datetime(2023, 1, 1)
        
        self.SetStartDate(self.start_date)
        self.SetEndDate(self.end_date)
        self.SetCash(1000000)
        
        self.current_holdings = 0
        self.target_holdings = 0
        self.sample_size = 50
        self.SetWarmup(-1)

        self.alpha1 = 0.2
        self.alpha2 = -0.2

        self.timer1 = []
        self.timer2 = []
        
        # Requesting data
        self.aapl = self.AddEquity("AAPL", Resolution.Minute).Symbol
        self.tiingo_symbol = self.AddData(TiingoNews, self.aapl, resolution=Resolution.Minute).Symbol

        self.num_bull = 0
        self.num_neu = 0
        self.num_bear = 0
        
        # Historical data
        # history = self.History(self.tiingo_symbol, start = self.start_date, end = self.end_date, resolution = Resolution.Daily)
        self.prev_price = 0
        self.sentiments = []

        file = self.Download("https://www.dropbox.com/scl/fi/n9y784pd2zumle5v6umv7/news_score_apple_2022_3.csv?rlkey=n97ctcjuab31qse9lvdnel6yj&dl=1")
        
        self.score_df = pd.read_csv(StringIO(file))

        # file = StringIO(csv)
        # self.score_df = pd.read_csv(csv)
        # self.Debug(file.read())
        # self.score_df = pd.read_csv(file, on_bad_lines='skip')
        # self.Debug(self.score_df)
        self.score_dic = self.score_df.set_index('date')['score'].to_dict()
        
        
    def OnData(self, slice: Slice) -> None:
        cur_time = self.Time
        if self.timer1:
            to_sell1 = 0
            for t in self.timer1:
                if (cur_time - t) > timedelta(hours=1):
                    to_sell1 += 1
            self.timer1 = self.timer1[to_sell1:]
            self.target_holdings = self.alpha1 * to_sell1

        if self.timer2:
            to_sell2 = 0
            for t in self.timer2:
                if (cur_time - t) > timedelta(hours=1):
                    to_sell2 += 1
            self.timer2 = self.timer2[to_sell2:]
            self.target_holdings = self.alpha2 * to_sell2

        if slice.ContainsKey(self.tiingo_symbol):
            title_words = slice[self.tiingo_symbol].Title + slice[self.tiingo_symbol].Description
            cur_time = f"{self.Time}"
            if cur_time in self.score_dic:
                score = self.score_dic[cur_time]
                # self.Debug(f"{cur_time} {score}")
                if score == 1:
                    self.target_holdings += self.alpha1
                    self.timer1.append(self.Time)
                if score == -1:
                    self.target_holdings += self.alpha2
                    self.timer2.append(self.Time)
        else:
            if self.current_holdings != self.target_holdings:
                self.SetHoldings(self.aapl, self.target_holdings)
                self.current_holdings = self.target_holdings


    # def OnEndOfAlgorithm(self):
    #     self.Debug(f"Number of Bullish: {self.num_bull}, Number of Neutral: {self.num_neu}, Number of Bearish: {self.num_bear}")