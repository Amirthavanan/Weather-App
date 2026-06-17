import requests

def get_country_info(country_name):
    url = f"https://restcountries.com/v3.1/name/{country_name}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            return data[0]
        return {"error": "Country data not found."}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
