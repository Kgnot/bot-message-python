import json

def clean_json(response_text: str):
    cleaned = response_text.replace("```json", "").replace("```", "").strip()
    return json.loads(cleaned)

def merge_json(a: dict, b: dict) -> dict:
    return {**a, **b}


