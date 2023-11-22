#region imports
from AlgorithmImports import *
import numpy as np
import openai
#endregion

import pandas as pd
from gpt_prompt import get_sentiment_general, get_sentiment_general_parallel, get_sentiment_general_sequence
import time


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

        self.alpha1 = 0.1
        self.alpha2 = 0.5
        
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
        
    def OnEndOfDay(self):
        pass
        
    def OnData(self, slice: Slice) -> None:
        if slice.ContainsKey(self.tiingo_symbol):
            title_words = slice[self.tiingo_symbol].Title + slice[self.tiingo_symbol].Description
            self.Debug(title_words)

    def OnEndOfMinute(self):
        pass


    def OnEndOfAlgorithm(self):
        self.Debug(f"Number of Bullish: {self.num_bull}, Number of Neutral: {self.num_neu}, Number of Bearish: {self.num_bear}")