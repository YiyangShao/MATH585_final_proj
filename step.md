## Analyze Sentiment Analysis

- (Finished) Speed up running time 
- (Finish NLTK) Compare GPT sentiment with other sentiment analysis tools
- Design an experiment based on sentiment result v.s. future return
- Try prompt engineering: use rate 1-10
- crawl time v.s. publish time

### Improve speeding up
May need to build a backend server for QuantConnect

### Improve model analysis
Get a larger dataset
Get another model
Get GPT4



## Design a strategy based on sentiment

- buffer of 100 news
 


## Good News
1. GPT-4 turbo has a stronger, cheaper version
2. GPT-4 api is very quick, 0.1 request/s
3. Token limits for gpt-4 turbo is large
4. GPT-3.5-16k seems more reliable
5. Rate for GPT-4 $0.15/200news

## Challenges:
1. GPT-4 is still expensive
2. GPT-3.5 is slow and unreliable
3. can't get financial news data out
4. GPT-4 turbo has knowledge up to 11/6

## Solution:
1. Get the news data only once
2. use the data for future training

## Experiment:
10 news/day, 20 days, 26s, gpt-3.5-turbo-1106
50 news/day, 20 days, 58s, gpt-3.5-turbo-1106

## Backtest
https://www.quantconnect.com/terminal/processCache?request=embedded_backtest_cf36bec6abad9b316eaca81f536385ff.html



## Update by 11/22
1. Only way to prevent lookahead: Temporal Awareness in Queries
2. Oldest Model in GPT-3: Oct 2019
3. Get data from logs
4. 2021 model and 2023 model has 80% similarity on 2022 news data


## Next Step for 11/22:
1. what model is good for sentiment score
2. paper p15
3. get price change(return) for different lags
4. get correlation for risk level and price change