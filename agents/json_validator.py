def validate_json(data):

    required_keys = ["disease", "diet", "nutrition", "recipes"]

    if not isinstance(data, dict):
        return False

    return all(key in data for key in required_keys)