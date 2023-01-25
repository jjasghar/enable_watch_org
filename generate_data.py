# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from datetime import datetime
from random import randint
from time import sleep
from requests.exceptions import HTTPError
import requests

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import logging

logging.basicConfig(filename='./static/out.log',level=logging.INFO)
logger = logging.getLogger(__name__)

def get_repos(params):
    # define the gql query
    query = gql(
        """
    query RepoCount($cursor: String, $org: String!) {
        organization(login: $org) {
        repositories(first: 10, after: $cursor) {
            pageInfo {
            hasNextPage
            endCursor
            }
            nodes {
            name
            }
        }
        }
    }
    """
    )

    response = client.execute(query, variable_values=params)
    return response

def build_list(org, gh_token):
    ORG = org
    GH_TOKEN = gh_token
    all_repos = []
    endCursor = None

    # Create a GraphQL client using the defined transport
    transport = RequestsHTTPTransport(url="https://api.github.com/graphql",
                              verify=True, retries=3,
                              headers={'Authorization': 'token ' + GH_TOKEN,
                                       'User-Agent': 'request'})
    global client
    client = Client(transport=transport, fetch_schema_from_transport=True)

    while True:
        params = {"cursor": endCursor, "org": ORG}
        try:
            response = get_repos(params)
        except Exception as e:
            rand_sleep = randint(5, 30)
            payload_requests = {
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {GH_TOKEN}",
                "X-GitHub-Api-Version": "2022-11-28" 
            }
            rate_limit_response = requests.get("https://api.github.com/rate_limit", json=payload_requests)
            rate_limit_response_json = rate_limit_response.json()
            if rate_limit_response_json['resources']['core']['remaining'] not in range(55, 60):
                logger.error(f"Gonna sleep for {rand_sleep} seconds because of a this error ---> {e}")
                sleep(rand_sleep)
            continue

        repos = response['organization']['repositories']['nodes']
        all_repos = all_repos + repos
        hasNextPage = response['organization']['repositories']['pageInfo']['hasNextPage']
        endCursor = response['organization']['repositories']['pageInfo']['endCursor']

        logger.info(f"Getting {len(all_repos)} of the repositories")
        if not hasNextPage:
            break

    return all_repos