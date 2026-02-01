# Returns a random node in sample.json for testing purposes.

async def generate_node(character_id, run_id):
    import json
    import random

    # Select a random number between 0 and 1
    rand_index = random.randint(0, 1)

    # Load sample data from JSON file
    with open("./data/sample.json", "r") as f:
        SAMPLE_DATA = json.load(f)

    return_payload = SAMPLE_DATA[rand_index]
    return return_payload