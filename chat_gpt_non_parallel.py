import os
import openai
import time

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
os.environ['API_KEY'] = ""
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


t0 = time.time()
for i in range(50):
    prompt = "What is 1 + 1"
    response, tokens = get_completion(prompt)
t1 = time.time()

print(f"tokens: {tokens}, average running time: {(t1-t0)/50:.2f} second")