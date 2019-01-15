import requests


class CodeClimate:

    API_BASE_URL = 'https://api.codeclimate.com'

    def __init__(self, api_token: str):
        self._api_token = api_token

    def _build_uri(self, resource):
        return '{}/{}'.format(self.API_BASE_URL, resource)

    def _get_base_header(self):
        return {
            'Accept': 'application/vnd.api+json',
            'Authorization': 'Token token={}'.format(self._api_token)
        }

    def get_organizartions(self):
        uri = self._build_uri('v1/orgs')
        headers = self._get_base_header()
        response = requests.get(uri, headers=headers)

        return response.json()['data']

    def add_private_repository(self, organization_id, repository_url):
        uri = self._build_uri('v1/orgs/{}/repos'.format(organization_id))
        headers= self._get_base_header()
        headers.update({
            'Content-Type': 'application/vnd.api+json'
        })

        payload = {
            "data": {
                "type": "repos",
                "attributes": {
                    "url": repository_url
                }
            }
        }

        response = requests.post(uri, headers=headers, json=payload)
        return response.json()['data']
