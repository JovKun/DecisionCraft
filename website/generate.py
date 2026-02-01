# Define the ruleset for content generation
ruleset = "Make sure that any generated content is short, consise and not overly verbose. The generated content should be based from the previous choices from the user, and it should reflect the changes made. For example, if a choice avoids a war and the next character is a part of such war, then the next round of choices should reflect that change. If the choices do not contradict such changes, then the generated choices should be as close to historically accurate as possible with respect to the characters' personalities and ideals. For example, assume that Hitler will always do what he did no matter the previous choices. Ensure that the generated content is historically plausible and does not contain hallucinations. Also, when asked about generating choices, make sure you only generate three lines with no extra new lines; nothing more and nothing less."

# Import necessary libraries
import asyncio
from flask import json, jsonify
from dotenv import load_dotenv

import requests
import os
import hashlib
import json as pyjson

from server.fallback import fallback_payload
from server.validation import validate_node_payload
load_dotenv()

def make_cache_key(run_id, character_id, previous_results):
    payload = {
        "run_id": run_id,
        "character_id": character_id,
        "previous_results": previous_results
    }
    s = pyjson.dumps(payload, sort_keys=True, separators=("," , ":")).encode('utf-8')
    return hashlib.sha256(s).hexdigest()

# Define constants for API interaction
API_URL = "https://models.github.ai/inference/chat/completions"
TOKEN = os.getenv("GITHUB_API_TOKEN")
MAX_ATTEMPTS = 5

GEN_CACHE = {}

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2024-06-05",
    "Content-Type": "application/json"
}

# Load character data from JSON file
with open("./data/characters.json", "r") as f:
    RAW_DATA = json.load(f)

CHARACTER_DATA = {char["id"]: char for char in RAW_DATA}

previous_results = []

# Generates a node based on the character ID
async def generate_node(character_id, run_id):
    

    # Prepare prompts
    prompt_prompt = f"Ask the user what they would do if they were the historical figure {CHARACTER_DATA[character_id]['figure']} in {CHARACTER_DATA[character_id]['year']} based on the previous choices: {previous_results}. If there are previous results, also add a brief description of how those results have affected the current situation."
    context_prompt = f"Generate a sentence-long context providing background information relevant to the prompt about {CHARACTER_DATA[character_id]['figure']} in {CHARACTER_DATA[character_id]['year']}. Consider all previous results: {previous_results}."
    choices_prompt = f"Generate 3 distinct choices for the following prompt: {prompt_prompt} Consider all previous results: {previous_results}."

    # Generate prompt
    payload = {
        "model": "openai/gpt-4o",
        "messages": [
            {
                "role": "system",
                "content": ruleset
            },
            {
                "role": "user",
                "content": prompt_prompt
            }
        ]
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    prompt = data.get("choices")[0].get("message").get("content")

    # Generate context
    payload["messages"][1]["content"] = context_prompt
    context_response = requests.post(API_URL, headers=headers, json=payload)
    context_response.raise_for_status()
    context_data = context_response.json()
    context = context_data.get("choices")[0].get("message").get("content")

    # Generate choices
    payload["messages"][1]["content"] = choices_prompt
    choices_response = requests.post(API_URL, headers=headers, json=payload)
    choices_response.raise_for_status()
    choices_data = choices_response.json()
    choices = choices_data.get("choices")[0].get("message").get("content")

    last_errors = []

    for attempt in range(MAX_ATTEMPTS):

        # Define the return payload and return it
        return_payload = {
            "run_id": run_id,
            "year": CHARACTER_DATA[character_id]['year'],
            "leader": {
                "id": CHARACTER_DATA[character_id]['id'],
                "name": CHARACTER_DATA[character_id]['figure']
            },
            "node": {
                "id": character_id,
                "prompt": prompt,
                "context": context,
                "choices": [
                    {"id": f"choice_{i+1}", "text": choice.strip()}
                    for i, choice in enumerate(choices.split('\n') if choices else [])
                ]
            }
        }

        # Validate the generated payload
        ok, errors = validate_node_payload(return_payload)

        if ok:
            return return_payload
        
        last_errors.append(errors)
        print(last_errors)

    # Print fallback message and return fallback payload if max attempts reached
    print("Max attempts reached. Returning last payload with errors.")
    fb = fallback_payload(
        run_id,
        CHARACTER_DATA[character_id]['year'],
        CHARACTER_DATA[character_id]['id'],
        CHARACTER_DATA[character_id]['figure']
    )
    return fb

# Given a payload and the user's choice, add the result to previous_results, which only holds the chosen choice
def add_previous_result(payload, choice_id):
    node = payload.get("node", {})
    choices = node.get("choices", [])
    selected_choice = next((choice for choice in choices if choice.get("id") == choice_id), None)

    if selected_choice:
        previous_results.append(selected_choice.get("text"))

# Test the function if run as main
if __name__ == "__main__":
    result = asyncio.run(generate_node(1, 1))
    print(json.dumps(result, indent=2))