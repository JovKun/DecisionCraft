import json

# Returns a random node in sample.json for testing purposes.
CURRENT_ID = 1

async def generate_node(character_id, run_id):

    global CURRENT_ID

    # Load sample data from JSON file
    with open("./data/sample.json", "r") as f:
        SAMPLE_DATA = json.load(f)

    result = SAMPLE_DATA[CURRENT_ID - 1]
    CURRENT_ID += 1
    return result