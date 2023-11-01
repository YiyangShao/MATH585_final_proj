#region imports
from AlgorithmImports import *
import numpy as np
import openai
#endregion

import pandas as pd
from gpt_prompt import get_sentiment_general, get_sentiment_general_parallel


class TiingoNewsDataAlgorithm(QCAlgorithm):

    def Initialize(self) -> None:
        self.start_date = datetime(2021, 3, 29)
        self.end_date = datetime(2021, 3, 30)
        
        self.SetStartDate(self.start_date)
        self.SetEndDate(self.end_date)
        self.SetCash(1000000)
        
        self.current_holdings = 0
        self.target_holdings = 0
        self.SetWarmup(-1)
        
        # Requesting data
        self.aapl = self.AddEquity("AAPL", Resolution.Minute).Symbol
        self.tiingo_symbol = self.AddData(TiingoNews, self.aapl, resolution=Resolution.Minute).Symbol
        
        # Historical data
        history = self.History(self.tiingo_symbol, start = self.start_date, end = self.end_date, resolution = Resolution.Daily)
        self.Debug(f"We got {len(history)} items from our history request")
        self.sentiments = []
        
        
        
    def OnData(self, slice: Slice) -> None:
        if slice.ContainsKey(self.tiingo_symbol):
            return
        self.Debug(f"{slice.Time}")
        if self.current_holdings != self.target_holdings:
            # self.Debug(f"Traded {self.current_holdings} {self.target_holdings}")
            self.SetHoldings(self.aapl, self.target_holdings)
            self.current_holdings = self.target_holdings

