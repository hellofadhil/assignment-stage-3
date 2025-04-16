import json

def fetch_drone_data():
    try:
        with open('./data.json', 'r') as file:
            data = json.load(file)
            return data
    except Exception as e:
        print(f"Error reading drone data: {e}")
        return []
