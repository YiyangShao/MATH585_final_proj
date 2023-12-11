

import os
import openai
import time

from dotenv import load_dotenv, find_dotenv
from multiprocessing import Pool
from itertools import repeat



def get_sentiment_general(news, model="gpt-3.5-turbo", company=None, output="polar", explanation=False):
    _ = load_dotenv(find_dotenv())
    openai.api_key  = os.getenv('API_KEY')   
    if company:
        company_prompt = f"for {company}" 
    else:
        company_prompt = ""
    if explanation:
        explanation_prompt = f"Your answer will include 2 lines. In the first line, you will answer 1 sentence to analyze why the news is good or bad {company_prompt}."
        explanation_addup = "in the second line, "
    else:
        explanation_prompt = "You will not give explanation to your answer."
        explanation_addup = ""
        
    if output == "polar":
        output_prompt = f"Then, {explanation_addup}you will answer with: BEARISH, BULLISH, NEUTRAL."
    elif output =="score":
        output_prompt = f"Then, {explanation_addup}you will answer with an integer between 1 and 10, with 1 being most BEARISH, 10 being most BULLISH."
    else:
        output_prompt = f"Then, {explanation_addup}you will answer with an integer between 1 and 10, with 1 being most BEARISH, 10 being most BULLISH."
        
    system_analysis_prompt =  f"You will work as a Sentiment Analysis Expert for Financial News {company_prompt}, focusing on financial indicators such as earnings, market trends, and investor opinions. {explanation_prompt} {output_prompt}"
    print(system_analysis_prompt)
    messages = []
    messages = [{"role": "system", "content": system_analysis_prompt}]
    messages.append({"role": "user", "content":news})
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    response_message = response.choices[0].message["content"]
    # tokens = response.usage["total_tokens"]
    if explanation:
        ans = response_message.split("\n")
        if len(ans) == 1:
            ans = response_message.split(" ")
            output = ans[-1]
            reason = " ".join(ans[:-1])
        else:
            reason = ans[0]
            output = ans[-1]
        
    else:
        output = response_message
        reason = ""
    
    return output, reason


def get_sentiment_general_multiple(news_list, model="gpt-3.5-turbo", company=None, output="polar", explanation=False, threads=10):
    _ = load_dotenv(find_dotenv())
    openai.api_key  = os.getenv('API_KEY')   
    if company:
        company_prompt = f"for {company}" 
    else:
        company_prompt = ""
    if explanation:
        explanation_prompt = f"Your answer will include 2 lines. In the first line, you will answer 1 sentence to analyze why the news is good or bad {company_prompt}."
        explanation_addup = "in the second line, "
    else:
        explanation_prompt = "You will not give explanation to your answer."
        explanation_addup = ""
        
    if output == "polar":
        output_prompt = f"Then, {explanation_addup}you will answer with: BEARISH, BULLISH, NEUTRAL."
    elif output =="score":
        output_prompt = f"Then, {explanation_addup}you will answer with an integer between 1 and 10, with 1 being most BEARISH, 10 being most BULLISH."
    else:
        output_prompt = f"Then, {explanation_addup}you will answer with an integer between 1 and 10, with 1 being most BEARISH, 10 being most BULLISH."
        
    system_analysis_prompt =  f"You will work as a Sentiment Analysis for Financial News {company_prompt}. {explanation_prompt} {output_prompt}"
    messages = []
    messages = [{"role": "system", "content": system_analysis_prompt}]
    for news in news_list:
        messages.append({"role": "user", "content":news})
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    print(response)
    response_message = response.choices[0].message["content"]
    if explanation:
        ans = response_message.split("\n")
        if len(ans) == 1:
            ans = response_message.split(" ")
            output = ans[-1]
            reason = " ".join(ans[:-1])
        else:
            reason = ans[0]
            output = ans[-1]
        
    else:
        output = response_message
        reason = ""
    
    return output, reason



def get_sentiment_general_parallel(news_list, model="gpt-3.5-turbo", company=None, output="polar", explanation=False, threads=10):
    t0 = time.time()
    with Pool(threads) as p:
        pool_output = p.starmap(get_sentiment_general, zip(news_list, repeat(model), repeat(company), repeat(output), repeat(explanation)))
    t1 = time.time()
    print(f" average running time: {(t1-t0)/len(news_list):.2f} second")
    return pool_output


def get_sentiment_general_sequence(news_list, model="gpt-3.5-turbo", company=None, output="polar", explanation=False, threads=10):
    t0 = time.time()
    pool_output = []
    for i in range(len(news_list)):
        pool_output.append(get_sentiment_general(news_list[i], model, company, output, explanation))
    t1 = time.time()
    print(f" average running time: {(t1-t0)/len(news_list):.2f} second")
    return pool_output



def get_risk_score(news, model="gpt-3.5-turbo", company=None, output="score", explanation=False):
    _ = load_dotenv(find_dotenv())
    openai.api_key  = os.getenv('API_KEY')   
    if company:
        company_prompt = f"for {company}" 
    else:
        company_prompt = ""
    if explanation:
        explanation_prompt = f"Your answer will include 2 lines. In the first line, you will answer 1 sentence to give solid reason why the news is highly risky {company_prompt}."
        explanation_addup = "in the second line, "
    else:
        explanation_prompt = "You will not give explanation to your answer."
        explanation_addup = ""
        
    if output == "polar":
        output_prompt = f"Then, {explanation_addup}you will answer with: **HIGH RISK** or **LOW RISK**"
    elif output =="score":
        output_prompt = f"Then, {explanation_addup}you will answer with an integer between 1 and 100, with 1 being most safe, 100 being most risky."
   
    system_analysis_prompt =  f"You will work as a Risk Management Expert for Financial News {company_prompt}. {explanation_prompt} {output_prompt}"
    messages = []
    messages = [{"role": "system", "content": system_analysis_prompt}]
    messages.append({"role": "user", "content":news})
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    response_message = response.choices[0].message["content"]
    if explanation:
        ans = response_message.split("\n")
        if len(ans) == 1:
            ans = response_message.split(" ")
            output = ans[-1]
            reason = " ".join(ans[:-1])
        else:
            reason = ans[0]
            output = ans[-1]
        
    else:
        output = response_message
        reason = ""
    
    return output, reason

def get_risk_score_parallel(news_list, model="gpt-3.5-turbo", company=None, output="score", explanation=False, threads=10):
    t0 = time.time()
    with Pool(threads) as p:
        pool_output = p.starmap(get_risk_score, zip(news_list, repeat(model), repeat(company), repeat(output), repeat(explanation)))
    t1 = time.time()
    print(f" average running time: {(t1-t0)/len(news_list):.2f} second")
    return pool_output



def get_sentiment_conservative(news, model="gpt-3.5-turbo", company=None, output="polar", explanation=False):
    _ = load_dotenv(find_dotenv())
    openai.api_key  = os.getenv('API_KEY')   
    if company:
        company_prompt = f"for {company}" 
    else:
        company_prompt = ""
    if explanation:
        explanation_prompt = f"Your answer will include 2 lines. In the first line, you will answer 1 sentence to analyze why the news is good or bad {company_prompt}."
        explanation_addup = "in the second line, "
    else:
        explanation_prompt = "You will not give explanation to your answer."
        explanation_addup = ""
        
    if output == "polar":
        output_prompt = f"Then, {explanation_addup}you will answer with: BEARISH, BULLISH, NEUTRAL."
    elif output =="score":
        output_prompt = f"Then, {explanation_addup}you will answer with an integer between 1 and 10, with 1 being most BEARISH, 10 being most BULLISH."
    else:
        output_prompt = f"Then, {explanation_addup}you will answer with an integer between 1 and 10, with 1 being most BEARISH, 10 being most BULLISH."
        
    system_analysis_prompt =  f"You will work as a Sentiment Analysis for Financial News {company_prompt}. You will be a little conservative on your perspective. {explanation_prompt} {output_prompt}"
    messages = []
    messages = [{"role": "system", "content": system_analysis_prompt}]
    messages.append({"role": "user", "content":news})
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    response_message = response.choices[0].message["content"]
    if explanation:
        ans = response_message.split("\n")
        if len(ans) == 1:
            ans = response_message.split(" ")
            output = ans[-1]
            reason = " ".join(ans[:-1])
        else:
            reason = ans[0]
            output = ans[-1]
        
    else:
        output = response_message
        reason = ""
    
    return output, reason

def get_sentiment_conservative_parallel(news_list, model="gpt-3.5-turbo", company=None, output="polar", explanation=False, threads=10):
    t0 = time.time()
    with Pool(threads) as p:
        pool_output = p.starmap(get_sentiment_conservative, zip(news_list, repeat(model), repeat(company), repeat(output), repeat(explanation)))
    t1 = time.time()
    print(f" average running time: {(t1-t0)/len(news_list):.2f} second")
    return pool_output


class Prompt:
    def __init__(self):
        _ = load_dotenv(find_dotenv())
        openai.api_key  = os.getenv('API_KEY')      
    
    
    def get_completion(self, prompt, model="gpt-3.5-turbo"):
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0,
        )
        tokens = response.usage["total_tokens"]
        return response.choices[0].message["content"], tokens


    def get_sentiment_completion(self, news, model="gpt-3.5-turbo"):
        system_analysis_prompt =  "You will work as a Sentiment Analysis for Financial News. \
            You will only answer as: \n\n BEARISH, BULLISH, NEUTRAL. No further explanation=."
        messages = []
        messages = [{"role": "system", "content": system_analysis_prompt}]
        messages.append({"role": "user", "content":news})
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0,
        )
        return response.choices[0].message["content"]
    
    def get_sentiment_completion_company(self, news, company, model="gpt-3.5-turbo"):
        system_analysis_prompt =  "You will work as a Sentiment Analysis for Financial News for Apple. \
            You will only answer as: \n\n BEARISH, BULLISH, NEUTRAL. No further explanation=."
        messages = []
        messages = [{"role": "system", "content": system_analysis_prompt}]
        messages.append({"role": "user", "content":news})
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0,
        )
        return response.choices[0].message["content"]
    
    def get_sentiment_completion_company(self, news, company, model="gpt-3.5-turbo"):
        system_analysis_prompt =  "You will work as a Sentiment Analysis for Financial News for Apple. \
            You will only answer as: \n\n BEARISH, BULLISH, NEUTRAL. No further explanation=."
        messages = []
        messages = [{"role": "system", "content": system_analysis_prompt}]
        messages.append({"role": "user", "content":news})
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0,
        )
        return response.choices[0].message["content"]
    
    
    def get_sentiment_completion_company(self, news, company, model="gpt-3.5-turbo"):
        system_analysis_prompt =  f"You will work as a Sentiment Analysis for Financial News for {company}. \
            You will only answer as: \n\n BEARISH, BULLISH, NEUTRAL. No further explanation=."
        messages = []
        messages = [{"role": "system", "content": system_analysis_prompt}]
        messages.append({"role": "user", "content":news})
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0,
        )
        return response.choices[0].message["content"]
    
    def get_sentiment_completion_company_score(self, news, company, model="gpt-3.5-turbo"):
        system_analysis_prompt =  f"You will work as a Sentiment Analysis for Financial News for {company}. \
            You will only answer with a number between 0 and 10, with 0 being most BEARISH, 10 being most BULLISH. No further explanation=."
        messages = []
        messages = [{"role": "system", "content": system_analysis_prompt}]
        messages.append({"role": "user", "content":news})
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0,
        )
        return response.choices[0].message["content"]
    
    def get_sentiment_completion_company_score_explanation(self, news, company, model="gpt-3.5-turbo"):
        system_analysis_prompt =  f"You will work as a Sentiment Analysis for Financial News for {company}. \
            You will first analyze whether the news is good or bad for {company} in 1 sentence \
            Then, You will only answer with a number between 1 and 10, with 1 being most BEARISH, 10 being most BULLISH."
        messages = []
        messages = [{"role": "system", "content": system_analysis_prompt}]
        messages.append({"role": "user", "content":news})
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0,
        )
        return response.choices[0].message["content"]
    

    
    def test(self):
        print("test")