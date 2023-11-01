#region imports
from AlgorithmImports import *
import numpy as np
import openai
#endregion

import pandas as pd
from gpt_prompt import get_sentiment_general, get_sentiment_general_parallel


class TiingoNewsDataAlgorithm(QCAlgorithm):

    def Initialize(self) -> None:
        self.SetStartDate(2021, 3, 29)
        self.SetEndDate(2021, 3, 30)
        self.SetCash(1000000)
        self.current_holdings = 0
        self.target_holdings = 0
        self.SetWarmup(-1)
        # Requesting data
        self.aapl = self.AddEquity("AAPL", Resolution.Minute).Symbol
        self.tiingo_symbol = self.AddData(TiingoNews, self.aapl, resolution=Resolution.Minute).Symbol
        
        # Historical data
        # history = self.History(self.tiingo_symbol, 5, Resolution.Daily)
        # self.Debug(f"We got {len(history)} items from our history request")
        openai.api_key = "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"
        self.sentiments = []
        
        
        
    def OnData(self, slice: Slice) -> None:
        if slice.ContainsKey(self.tiingo_symbol):
            title_words = slice[self.tiingo_symbol].Description
            response = get_sentiment_general(title_words)[0]
            score = 0
            if response == "BULLISH":
                score = 1
            elif response == "BEARISH":
                score = -1
            elif response == "NEUTRAL":
                score = 0
            
            self.sentiments.append(score)
            if len(self.sentiments) > 100:
                self.sentiments.pop(0)
            self.target_holdings = sum(self.sentiments)/100
            self.Debug(f"{score} {self.target_holdings}")

            if score > 0:
                self.target_holdings = 1
            elif score < 0:
                self.target_holdings = -1
            else:
                self.target_holdings = 0
            
            self.Debug(f"{score} {response} {title_words} score")
        
        if self.current_holdings != self.target_holdings:
            # self.Debug(f"Traded {self.current_holdings} {self.target_holdings}")
            self.SetHoldings(self.aapl, self.target_holdings)
            self.current_holdings = self.target_holdings

