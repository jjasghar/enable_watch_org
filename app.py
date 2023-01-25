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

from flask import Flask, render_template, request, url_for, flash, redirect
from generate_data import build_list
from fix_repo_status import send_fix_request
import os
import logging
from version import get_version

logging.basicConfig(filename='./static/out.log',level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('APP_SECRET_KEY')

repo_list = []

@app.route('/')
def index():
    return render_template('index.html', version=get_version())

@app.route('/about')
def about():
    return render_template('about.html', version=get_version())

@app.route('/run/', methods=('GET', 'POST'))
def run():
    if request.method == 'POST':
        org = request.form['githuborg']
        gh_token = request.form['githubtoken']

        if not org:
            flash('GitHub Organization is required!')
        elif not gh_token:
            flash('A GitHub Token is required!')
        else:
            repo_list = build_list(org, gh_token)
            for repo in repo_list:
                send_fix_request(gh_token, repo, org)
            return render_template('index.html', repo_list=repo_list, ran=True, total_repos=len(repo_list), org=org, version=get_version())
    return render_template('run.html', version=get_version())