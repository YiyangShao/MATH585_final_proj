import os
import openai
import time

from dotenv import load_dotenv, find_dotenv
from multiprocessing import Pool

_ = load_dotenv(find_dotenv())
openai.api_key  = os.getenv('API_KEY')


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    tokens = response.usage["total_tokens"]
    return response.choices[0].message["content"], tokens



if __name__ == '__main__':
    t0 = time.time()
    prompt = "What is 1 + 1"
    with Pool(10) as p:
        print(p.map(get_completion, [prompt] * 50))
    t1 = time.time()
    print(f" average running time: {(t1-t0)/50:.2f} second")