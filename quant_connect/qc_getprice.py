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

        # if self.Securities[self.aapl].Price != 0 :
        #     self.return_per = (self.Securities[self.aapl].Price - self.last_day_price) / self.last_day_price
        #     self.last_day_price = self.Securities[self.aapl].Price
        #     self.Debug(f"Return is {self.return_per} at {self.Time}")


        # history = self.History(self.tiingo_symbol, 1, Resolution.Daily) 
        # if history.shape[0] >= self.sample_size:
        #     sample = history.sample(self.sample_size)
        # else:
        #     sample = history
        # sample_list = []
        # for i in range(sample.shape[0]):
        #     sample_list.append(sample["title"][i] + sample["description"][i])
        # # response = get_sentiment_general_parallel(sample_list)
        # response = get_sentiment_general_parallel(sample_list, company = "JPM", model="gpt-3.5-turbo-1106")
        # dic_gpt = {"BULLISH" : 1, "NEUTRAL" : 0, "BEARISH" : -1,}
        # output = [dic_gpt[r[0]] for r in response]


        # self.Debug(f"{sample.iloc[0,:]}")
        # self.Debug(f"We got {sample.shape[0]} items from our history request at {self.Time}")
        # self.Debug(f"{response} {output}")
        # self.Debug(f"target holding is {2*(sum(output)/sample.shape[0]-0.5)} at {self.Time}")
        # self.Debug(f"evaluation score is {sum(output)/sample.shape[0]} at {self.Time}")
        # self.target_holdings = 2*(sum(output)/sample.shape[0]-0.5)
        # time.sleep(1)
        
    def OnData(self, slice: Slice) -> None:
        if slice.ContainsKey(self.tiingo_symbol):
            title_words = slice[self.tiingo_symbol].Title + slice[self.tiingo_symbol].Description
            # self.Debug(title_words)
            # if self.Securities[self.aapl].Price != 0 and self.prev_price != self.Securities[self.aapl].Price:
            #     self.prev_price = self.Securities[self.aapl].Price
            #     try:
            #         t0 = time.time()
            #         title_words = slice[self.tiingo_symbol].Title + slice[self.tiingo_symbol].Description
            #         response = get_sentiment_general(title_words, company = "AAPL", model="gpt-3.5-turbo-1106")
            #         response = response[0]
            #         t1 = time.time()
            #         self.Debug(f"{response}, {self.target_holdings}, {t1-t0} seconds, {self.Securities[self.aapl].Price} {self.Time}")
            #         dic_gpt = {"BULLISH" : 1, "NEUTRAL" : 0, "BEARISH" : -1,}
            #         if dic_gpt[response] == 1:
            #             self.num_bull += 1
            #         elif dic_gpt[response] == 0:
            #             self.num_neu += 1
            #         elif dic_gpt[response] == -1:
            #             self.num_bear += 1
            #         if dic_gpt[response] == 1 and self.target_holdings < 1:
            #             self.target_holdings += dic_gpt[response] * self.alpha1
            #         if dic_gpt[response] == -1 and self.target_holdings > -1:
            #             self.target_holdings += dic_gpt[response] * self.alpha2
            #     except:
            #         pass
            # if self.current_holdings != self.target_holdings:
            # # self.Debug(f"Traded {self.current_holdings} {self.target_holdings}")
            #     self.SetHoldings(self.aapl, self.target_holdings)
            #     self.current_holdings = self.target_holdings
        else:
            self.Debug(f"{self.Time} {self.Securities[self.aapl].Price}")


    def OnEndOfAlgorithm(self):
        self.Debug(f"Number of Bullish: {self.num_bull}, Number of Neutral: {self.num_neu}, Number of Bearish: {self.num_bear}")