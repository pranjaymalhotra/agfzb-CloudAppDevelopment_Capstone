import sys
import requests



def main(params):
    URL = params['cloudant_url'] + '/reviews/_design/api/_view/by-dealership?include_docs=True'
    if 'dealerId' in params.keys():
        URL = URL + '&key=' + str(int(params['dealerId']))
    req = requests.get(URL, auth=(params['cloudant_user'], params['cloudant_password']))
    if req.status_code != 200:
        return {
            'headers': {'Content-Type': 'application/json'},
            'statusCode': 500,
            'body': {'error' :req.text}
        }
    payload = req.json()
    if len(payload['rows']) <= 0:
        return {
            'headers': {'Content-Type': 'application/json'},
            'statusCode': 404,
            'body': []
        }
    return {
            'headers': {'Content-Type': 'application/json'},
            'statusCode': 200,
            'body': list(map(lambda d: d['doc'], payload['rows']))
        }
