
# Load libraries
import openai
from openai import OpenAI
import requests
import time
import tiktoken


# Set API token
with open("token.txt", "r") as tf:
    TOKEN = tf.read().strip()  # Removes unwanted newline characters


openai.api_key = TOKEN
openai.api_base = "https://api-gpt.jrc.ec.europa.eu/v1"

client = OpenAI(
        api_key = TOKEN,
        base_url = openai.api_base   )


# Define request function with a try-except block in case of timeout errors

def get_chat_response(prompt, seed, model, temperature):
    max_retries = 3
    retry_count = 0

    while retry_count < max_retries:
        start_time = time.time()
        try:
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=model,
                seed=seed,
                temperature=temperature
            )
            end_time = time.time()
            response_time = end_time - start_time
            return {
                "response_content": response.choices[0].message.content,
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.total_tokens - response.usage.prompt_tokens,
                "system_fingerprint": response.system_fingerprint,
                "response_time": response_time
            }
        except requests.exceptions.Timeout:
            retry_count += 1
            print(f"Timeout occurred. Retrying ({retry_count}/{max_retries})...")
            time.sleep(60)  # Wait for 1 minute before retrying
        except Exception as e:
            print(f"An error occurred: {e}")
            return None  # Return None if an unexpected error occurs

    print("Maximum retries exceeded. Unable to get a response.")
    return None


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


   


# List of GPT@JRC models available 
# all_models = client.models.list()
# chat_models = [model for model in all_models.data if model.model_usage == "chat"] # Filter the chat models

# for model in chat_models: # print all chat models
#     print(model)
#     print('--------')