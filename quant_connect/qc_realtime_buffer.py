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
        self.start_date = datetime(2020, 1, 1)
        self.end_date = datetime(2021, 1, 10)
        
        self.SetStartDate(self.start_date)
        self.SetEndDate(self.end_date)
        self.SetCash(1000000)
        
        self.current_holdings = 0
        self.target_holdings = 0
        self.sample_size = 50
        self.SetWarmup(-1)

        self.alpha1 = 0.1
        self.alpha2 = 0.5

        self.news_buffer = []
        self.thres = 10
        
        # Requesting data
        self.aapl = self.AddEquity("AAPL", Resolution.Minute).Symbol
        self.tiingo_symbol = self.AddData(TiingoNews, self.aapl, resolution=Resolution.Minute).Symbol
        
        # Historical data
        # history = self.History(self.tiingo_symbol, start = self.start_date, end = self.end_date, resolution = Resolution.Daily)
        self.last_day_price = 100
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
            if self.Securities[self.aapl].Price != 0:
                title_words = slice[self.tiingo_symbol].Title + slice[self.tiingo_symbol].Description
                if len(self.news_buffer) < self.thres:
                    self.news_buffer.append(title_words)
                else:
                    try:
                        response = get_sentiment_general_parallel(self.news_buffer, company = "AAPL", model="gpt-3.5-turbo-1106")
                        dic_gpt = {"BULLISH" : 1, "NEUTRAL" : 0, "BEARISH" : -1,}
                        to_move = 0
                        for r in reponse:
                            cur_news = dic_gpt[r[0]]
                            if cur_news < 0:
                                to_move -= self.alpha2
                            if cur_news > 0:
                                to_move += self.alpha1
                        to_move /= self.thres
                        self.Debug(f"{to_move}, {self.target_holdings} {self.Securities[self.aapl].Price} {self.Time}")
                        if to_move > 0 and self.target_holdings < 1:
                            self.target_holdings += to_move
                        if to_move < 0 and self.target_holdings > -1:
                            self.target_holdings += to_move
                    except:
                        pass
                    self.news_buffer = []
            if self.current_holdings != self.target_holdings:
            # self.Debug(f"Traded {self.current_holdings} {self.target_holdings}")
                self.SetHoldings(self.aapl, self.target_holdings)
                self.current_holdings = self.target_holdings

