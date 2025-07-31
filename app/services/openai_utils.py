from openai import OpenAI
import os
import requests

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def fetch_support_data(category: str) -> str:
    try:
        if category == "delivery":
            res = requests.get("")  # Replace with your delivery API URL
        elif category == "product":
            res = requests.get("")  # Replace with your product API URL
        elif category == "general":
            res = requests.get("")  # Replace with your general API URL
        else:
            return "No additional info available."

        if res.status_code == 200:
            return res.text
        else:
            return f"API error: {res.status_code}"
    except Exception as e:
        return f"Error fetching support data: {str(e)}"


def should_respond_and_generate_reply(body: str) -> tuple[bool, str]:
    classification_prompt = f"""
You are an AI support agent.

Given the following customer email, decide:
1. If it deserves a reply — reply with "yes" or "no"
2. What the topic is — choose one: delivery, product, general

Email:
{body}

Return:
should_respond: yes/no
category: delivery/product/general
"""
    classification_response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": classification_prompt}]
    ).choices[0].message.content.strip()

    lines = classification_response.splitlines()
    should_reply = "yes" in lines[0].lower()
    category = "general"

    for line in lines:
        if line.lower().startswith("category:"):
            category = line.split(":")[1].strip().lower()

    if not should_reply:
        return False, ""

    external_info = fetch_support_data(category)

    reply_prompt = f"""
You are a helpful customer support AI.

Here's the original customer email:
{body}

This is the information retrieved from our internal support API based on the topic "{category}":
{external_info}

Write a clear, polite and informative response to the customer using the above data.
"""
    reply = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": reply_prompt}]
    ).choices[0].message.content.strip()

    return True, reply

