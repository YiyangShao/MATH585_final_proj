#region imports
from AlgorithmImports import *
import numpy as np
import openai
#endregion


class TiingoNewsDataAlgorithm(QCAlgorithm):

    def Initialize(self) -> None:
        self.SetStartDate(2021, 6, 30)
        self.SetEndDate(2021, 6, 30)
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
        self.news_count = 0
        
        
    def OnData(self, slice: Slice) -> None:
        if slice.ContainsKey(self.tiingo_symbol):
            self.news_count += 1
            # # Assign a sentiment score to the news article
            # title_words =slice[self.tiingo_symbol].Title + slice[self.tiingo_symbol].Description
            title_words = slice[self.tiingo_symbol].Description
            response = self.get_sentiment_completion(title_words)
            score = 0
            if response == "BULLISH":
                score = 1
            elif response == "BEARISH":
                score = -1
            elif response == "NEUTRAL":
                score = 0
                    
            if score > 0:
                self.target_holdings = 1
                
            elif score < 0:
                self.target_holdings = -1
            
            else:
                self.target_holdings = 0
            
                self.Debug(f"{score} {response} {title_words} score {self.news_count}")
        
        if self.current_holdings != self.target_holdings:
            # self.Debug(f"Traded {self.current_holdings} {self.target_holdings}")
            self.SetHoldings(self.aapl, self.target_holdings)
            self.current_holdings = self.target_holdings

    def get_sentiment_completion(self, question, model="gpt-3.5-turbo"):
        system_analysis_prompt =  "You will work as a Sentiment Analysis for Financial News. \
            You will only answer as: \n\n BEARISH, BULLISH, NEUTRAL. No further explanation=."
        messages = []
        messages = [{"role": "system", "content": system_analysis_prompt}]
        messages.append({"role": "user", "content":question})
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0,
        )
        # print(response)
        return response.choices[0].message["content"]