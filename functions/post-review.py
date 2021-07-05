import sys
import requests

def main(params):
    URL = params['cloudant_url'] + '/reviews'
    if not 'review' in params.keys():
        return {
            'headers': {'Content-Type': 'application/json'},
            'statusCode': 500,
            'body': {'error' :'No review object in request'}
        }
    req = requests.post(URL, auth=(params['cloudant_user'], params['cloudant_password']), json=params['review'])
    if req.status_code > 400:
        return {
            'headers': {'Content-Type': 'application/json'},
            'statusCode': 500,
            'body': {'error' :req.text}
        }
    payload = req.json()
    return {
            'headers': {'Content-Type': 'application/json'},
            'statusCode': 200,
            'body': payload
    }
