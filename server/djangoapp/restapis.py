import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                            params=kwargs)
    except:
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def post_request(url, **kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    try:
        payload = kwargs.pop("payload")
        response = requests.post(url, headers={'Content-Type': 'application/json'},
                                            params=kwargs, json=payload)
    except:
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:

        dealers = json_result["entries"]
        # For each dealer object
        for dealer_doc in dealers:
            dealer_obj = CarDealer(
                address=dealer_doc["address"],
                city=dealer_doc["city"],
                full_name=dealer_doc["full_name"],
                id=dealer_doc["id"],
                lat=dealer_doc["lat"],
                long=dealer_doc["long"],
                short_name=dealer_doc["short_name"],
                st=dealer_doc["st"],
                zip=dealer_doc["zip"]
            )
            results.append(dealer_obj)

    return results

def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url)
    if json_result:
        reviews = json_result["entries"]
        for review_obj in reviews:
            review_obj = DealerReview(
                dealership=review_obj.get("dealership"),
                name=review_obj.get("name"),
                purchase=review_obj.get("purchase"),
                review=review_obj.get("review"),
                purchase_date=review_obj.get("purchase_date"),
                car_make=review_obj.get("car_make"),
                car_model=review_obj.get("car_model"),
                car_year=review_obj.get("car_year"),
                sentiment=analyze_review_sentiments(review_obj.get("review")),
                id=review_obj.get("id")
            )
            results.append(review_obj)

    return results

def store_review(url, payload):
    post_request(url, payload=payload)

def store_review(url, payload):
    post_request(url, payload=payload)


def analyze_review_sentiments(text):
    url = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/ea9342cf-1f2d-408d-8a92-2ce03dd249ea"
    api_key = "90lAvlUc2tQWaHAD9bRopwKh2DZUFKwVV3uiSZwPrEz_"
    params = {
        "text": text,
        "features": {
            "sentiment": {
            }
        },
        "language": "en"
    }
    response = requests.post(url, json=params, headers={'Content-Type': 'application/json'},
                                    auth=('apikey', api_key))
    return response.json()["sentiment"]["document"]["label"]



