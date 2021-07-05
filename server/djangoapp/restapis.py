import json
import os

import requests
from requests.auth import HTTPBasicAuth

from .models import CarDealer, DealerReview

URL_API = ''.join([
    'https://',
    'service.eu.apiconnect.ibmcloud.com',
    '/gws/apigateway/api',
    '/01b28f2350fa121cb3dd7a87ab47d8df4cdd102d0d53cfde82ed87d1b58b24d7',
    '/api'
])

WATSON_URL = ''.join([
    'https://',
    'api.eu-de.natural-language-understanding.watson.cloud.ibm.com',
    '/instances/62b5e198-cdd9-44c9-93e1-deb914502af3'
])

WATSON_API_KEY = os.environ.get('WATSON_API_KEY')

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        if 'api_key' in kwargs.keys():
            #api_key in params, use auth
            api_key = kwargs['api_key']
            del(kwargs['api_key'])
            response = requests.get(
                url,
                headers={
                    'Content-Type': 'application/json'
                },
                auth=HTTPBasicAuth('apikey', api_key),
                params=kwargs
                )
        else:
            #no api_key, don't authenticate
            response = requests.get(
                url,
                headers={
                    'Content-Type': 'application/json'
                },
                params=kwargs
                )
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    #print(response.text)
    #print(response.request.path_url)
    json_data = json.loads(response.text)
    return json_data

def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print("POST from {} ".format(url))
    try:
        if 'api_key' in kwargs.keys():
            #api_key in params, use auth
            api_key = kwargs['api_key']
            del(kwargs['api_key'])
            response = requests.post(
                url,
                headers={
                    'Content-Type': 'application/json'
                },
                auth=HTTPBasicAuth('apikey', api_key),
                params=kwargs,
                json=json_payload
                )
        else:
            #no api_key, don't authenticate
            response = requests.post(
                url,
                headers={
                    'Content-Type': 'application/json'
                },
                params=kwargs,
                json=json_payload
                )
    except:
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    #print(response.text)
    #print(response.request.path_url)
    json_data = json.loads(response.text)
    return response.json()

def get_dealers_from_cf(url = URL_API, **kwargs):
    results = []
    json_result = get_request(url + '/dealership', **kwargs)
    if json_result:
        for dealer_doc in json_result:
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

def get_dealer_by_id(dealerId, url = URL_API):
    url = url + '/dealership'
    return get_dealers_from_cf(url, id = dealerId)[0]

def get_dealer_by_state(state, url = URL_API):
    url = url + '/dealership'
    return get_dealers_from_cf(url, state=state)

def get_dealer_reviews_from_cf(dealerId, url = URL_API):
    def json_to_dealer_review(data):
        return DealerReview(
            id=data.get('id', ''),
            dealership=data['dealership'],
            review=data['review'],
            name=data.get('name', ''),
            purchase=data.get('purchase', ''),
            purchase_date=data.get('purchase_date', ''),
            car_make=data.get('car_make', ''),
            car_model=data.get('car_model', ''),
            car_year=data.get('car_year', ''),
            sentiment=analyze_review_sentiments(text=data['review'])
            )
    url = url + '/review'
    json_result = get_request(url, dealerId=dealerId)
    if len(json_result) > 0:
        reviews = list(map(json_to_dealer_review, json_result))
        return reviews
    return []

def analyze_review_sentiments(**kwargs):
    URL = WATSON_URL + '/v1/analyze'
    params = dict()
    params["text"] = kwargs["text"]
    params["version"] = '2021-03-25'
    params["features"] = 'sentiment'
    params["return_analyzed_text"] = 'false'
    params["api_key"] = WATSON_API_KEY
    response = get_request(
        URL,
        **params
    )
    return response["sentiment"]["document"]["label"]
