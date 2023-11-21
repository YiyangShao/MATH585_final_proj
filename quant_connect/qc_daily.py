#region imports
from AlgorithmImports import *
import numpy as np
import openai
#endregion

import pandas as pd
from gpt_prompt import get_sentiment_general, get_sentiment_general_parallel, get_sentiment_general_sequence


class TiingoNewsDataAlgorithm(QCAlgorithm):

    def Initialize(self) -> None:
        self.start_date = datetime(2021, 1, 1)
        self.end_date = datetime(2021, 2, 1)
        
        self.SetStartDate(self.start_date)
        self.SetEndDate(self.end_date)
        self.SetCash(1000000)
        
        self.current_holdings = 0
        self.target_holdings = 0
        self.sample_size = 50
        self.SetWarmup(-1)
        
        # Requesting data
        self.aapl = self.AddEquity("AAPL", Resolution.Minute).Symbol
        self.tiingo_symbol = self.AddData(TiingoNews, self.aapl, resolution=Resolution.Minute).Symbol
        
        # Historical data
        # history = self.History(self.tiingo_symbol, start = self.start_date, end = self.end_date, resolution = Resolution.Daily)
        
        self.sentiments = []
        
    def OnEndOfDay(self):
        history = self.History(self.tiingo_symbol, 1, Resolution.Daily) 
        if history.shape[0] >= self.sample_size:
            sample = history.sample(self.sample_size)
        else:
            sample = history
        sample_list = []
        for i in range(sample.shape[0]):
            sample_list.append(sample["title"][i] + sample["description"][i])
        # response = get_sentiment_general_parallel(sample_list)
        response = get_sentiment_general_parallel(sample_list, company = "Apple", model="gpt-3.5-turbo-1106")
        dic_gpt = {"BULLISH" : 1, "NEUTRAL" : 0, "BEARISH" : -1,}
        output = [dic_gpt[r[0]] for r in response]
        # self.Debug(f"{sample.iloc[0,:]}")
        # self.Debug(f"We got {sample.shape[0]} items from our history request at {self.Time}")
        # self.Debug(f"{response} {output}")
        self.Debug(f"target holding is {2*(sum(output)/sample.shape[0]-0.5)} at {self.Time}")
        self.target_holdings = 2*(sum(output)/sample.shape[0]-0.5)
        
    def OnData(self, slice: Slice) -> None:
        if slice.ContainsKey(self.tiingo_symbol):
            return
        if self.current_holdings != self.target_holdings:
            # self.Debug(f"Traded {self.current_holdings} {self.target_holdings}")
            self.SetHoldings(self.aapl, self.target_holdings)
            self.current_holdings = self.target_holdings

