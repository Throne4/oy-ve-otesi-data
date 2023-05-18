import requests, time
from rich import pretty, print
pretty.install()



cls = lambda: __import__("os").system("cls")



BASE_URL = "https://api-sonuc.oyveotesi.org"




def get_json(url : str, headers : dict = {}):
    _headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'tr-TR,tr;q=0.9',
        'origin': 'https://tutanak.oyveotesi.org',
        'referer': 'https://tutanak.oyveotesi.org/',
        'sec-ch-ua': '"Brave";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    }
    print(url)
    _headers.update(headers)
    try:
        response = requests.get(url, headers=_headers)
    except Exception as e:
        print(e, "Sleeping")
        time.sleep(2)
        return get_json(url, headers)
    if response.status_code == 429:
        time.sleep(2)
        return get_json(url, headers)
    try:
        return response.json()
    except Exception as e:
        print(e, "Sleeping")
        time.sleep(2)
        return get_json(url, headers)

cities = get_json(BASE_URL + "/api/v1/cities")


def get_districts(city_id : int):    
    return get_json(BASE_URL + f"/api/v1/cities/{city_id}/districts")

def get_neighborhoods(city_id : int, district_id : int):
    return get_json(BASE_URL + f"/api/v1/cities/{city_id}/districts/{district_id}/neighborhoods")

def get_neighborhood_results(neighbor_id : int):
    return get_json(BASE_URL + f"/api/v1/submission/neighborhood/{neighbor_id}")
    


total_votes = 0
candidates = {"rte" : 0, "ince" : 0, "kemal" : 0, "oğan" : 0}
for city in cities:
    if city["id"] == 82:
        continue
    districts = get_districts(city["id"])
    for district in districts:
        neighborhoods = get_neighborhoods(city["id"], district["id"])
        for neighborhood in neighborhoods:
            results = get_neighborhood_results(neighborhood["id"])
            for result in results:
                if not result.get("cm_result", {}):
                    result["cm_result"] = {}
                total_votes += result.get("cm_result",{}).get("total_vote", 0)
                candidates["rte"] += result.get("cm_result", {}).get("votes",{}).get("1", 0)
                candidates["ince"] += result.get("cm_result", {}).get("votes",{}).get("2", 0)
                candidates["kemal"] += result.get("cm_result", {}).get("votes",{}).get("3", 0)
                candidates["oğan"] += result.get("cm_result",{}).get("votes", {}).get("4", 0)
                if result.get("cm_result", {}).get("votes",{}).get("1", 0) + result.get("cm_result", {}).get("votes",{}).get("2", 0) + result.get("cm_result", {}).get("votes",{}).get("3", 0) + result.get("cm_result", {}).get("votes",{}).get("4", 0) != result.get("cm_result").get("total_vote", 0):
                    print("lol", city, district, neighborhood, result)
                print(candidates)
