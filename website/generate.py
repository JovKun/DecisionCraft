import json

async def generate_node(character_id, run_id):

    # Load sample data from JSON file
    with open("./data/sample.json", "r") as f:
        SAMPLE_DATA = json.load(f)

    result = SAMPLE_DATA[character_id - 1]
    return result