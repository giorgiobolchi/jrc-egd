
# Load libraries
import openai
from openai import OpenAI


# Set API token

with open("token.txt", "r") as tf:
 token = tf.read()

TOKEN = token
openai.api_base = "https://api-gpt.jrc.ec.europa.eu/v1"
openai.api_key = TOKEN

client = OpenAI(
        api_key = TOKEN,
        base_url = "https://api-gpt.jrc.ec.europa.eu/v1/"    )





# Define request function 
def get_chat_response(prompt,seed,model,temperature):

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=model, # usually "gpt-4o"
        seed=seed,  # to ensure consistency in responses and reproducability.
        temperature=temperature  # The temperature parameter influences the randomness of the generated responses. A higher value, such as 0.8, makes the answers more diverse, while a lower value, like 0.2, makes them more focused and deterministic.
        
    )
    response_content = response.choices[0].message.content
    system_fingerprint = response.system_fingerprint
    prompt_tokens = response.usage.prompt_tokens
    completion_tokens = response.usage.total_tokens - response.usage.prompt_tokens

    return {
            "response_content": response_content,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "system_fingerprint": system_fingerprint
        }
 



