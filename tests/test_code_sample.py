def process_user_data(user_id, data):
    """Process user data from API"""
    result = []
    for item in data:
        if item["status"] == "active":
            processed = transform_item(item)
            result.append(processed)
    return result


def transform_item(item):
    """Transform single item"""
    return {"id": item["id"], "value": item["value"] * 2, "timestamp": item["timestamp"]}


class DataManager:
    def __init__(self):
        self.cache = {}

    def get_data(self, key):
        if key in self.cache:
            return self.cache[key]
        data = self.fetch_from_db(key)
        self.cache[key] = data
        return data

    def fetch_from_db(self, key):
        # Simulate DB fetch
        return {"key": key, "value": "data"}
