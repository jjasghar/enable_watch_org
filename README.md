# enable_watch_org

## Scope

This is a simple helper application, to "watch"/"subscribe" every repository in a GitHub Organization. As of
the creation of this application, there is no way at an "org level" to watch every repository for a given namespace.

This means, if you are coming into a new organizanion, or have a "security" audit, you would have to walk through
each and every repository and click "watch" -> "all activity."

This application automates this, and also uses the [GraphQL](https://api.github.com/graphql) API endpoint, so you _shouldn't_
hit any of the standard REST API limits.

## Set up and Usage

1. Set up the dependancies.

```bash
git clone https://github.com/jjasghar/enable_watching_org.git
cd enable_watching_org
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

2. [Create a GitHub Token](https://github.com/settings/tokens) with the correct permissions. The Watching documentation is [here](https://docs.github.com/en/rest/activity/watching?apiVersion=2022-11-28). From what I can tell, you need at _least_ **notifications** permissions.

3. Run the application locally.

```bash
bash run_website_debug.sh
```
4. Open <http://127.0.0.1:5000>

## License & Authors

If you would like to see the detailed LICENSE click [here](./LICENSE).

- Author: JJ Asghar <awesome@ibm.com>

```text
Copyright:: 2023- IBM, Inc

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
