import requests

def safe_api_call(url, params=None):
    try:
        res = requests.get(url, params=params, timeout=5)

        if res.status_code == 200:
            return res.json()

        return None

    except Exception as e:
        print("⚠️ API Error:", e)
        return None