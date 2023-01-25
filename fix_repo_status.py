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

import requests
import logging

from requests.adapters import HTTPAdapter, Retry

logging.basicConfig(filename='./static/out.log',level=logging.INFO)
logger = logging.getLogger(__name__)

def send_fix_request(gh_token, repo, org):
  headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {gh_token}",
    "X-GitHub-Api-Version": "2022-11-28",
  }
  payload = {
    "subscribed": True,
    "ignored": False
  }

  s = requests.session()
  retries = Retry(total=5, backoff_factor=1, status_forcelist=[ 502, 503, 504 ])
  s.mount('https://', HTTPAdapter(max_retries=retries))
  name = repo['name']
  
  r = s.put(f"https://api.github.com/repos/{org}/{name}/subscription", headers=headers, json=payload)

  if r.ok:
    logging.info(f'Successfully fixed watch policy on {name}')
  else:
    logging.info(f'------> Something broke with {name}, spot check this one <-----')
