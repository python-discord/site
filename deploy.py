import os

import requests


branch = os.environ.get("TRAVIS_BRANCH")
url = os.environ.get("AUTODEPLOY_WEBHOOK")
token = os.environ.get("AUTODEPLOY_TOKEN")

if branch == 'master':
    print("deploying..")
    result = requests.post(url=url, headers={'token': token})
    print(result.text)

else:
    print("skipping deploy")
