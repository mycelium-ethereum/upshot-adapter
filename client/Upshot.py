import requests
from typing import (
    Dict, 
    Optional, 
    List
)

class Upshot:

    BASE_URL = "https://api.upshot.io/v1/"

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def parse_data(self, data: Dict) -> str:
        if data == {}: return ""
        msg = "?"
        for k, v in data.items(): msg += f"{k}={v}&"
        return msg[:-1]

    def request(self, endpoint: str, params: Dict = {}, method: str = 'GET'): 
        response = requests.request(
            method=method,
            url=self.BASE_URL + endpoint + self.parse_data(params),
            headers={'x-api-key': self.api_key})
        return response.json()

    def list_collections(self) -> List[str]:
        response = self.request(endpoint='collections')
        if response['status']:
            collections = response['data']['collections']
            return [{
                'name': c['name'], 
                'slug': c['slug']
            } for c in collections]
        else:
            print('Error', response['message'])
            return []

    def get_collection(self, collection_name: str) -> Dict:
        response = self.request(
            endpoint=f'collections/slug/{collection_name}',
            params={'includeStats': 'true'})
        if response['status']:
            if response['data']:
                return response['data']['stats']
            else:
                print('Invalid collection')
                return {}
        else:
            print(response['message'])
            return {}