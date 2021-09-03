import os

GIT_SHA = os.environ.get("GIT_SHA", "development")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
# How long to wait for synchronous requests before timing out
TIMEOUT_PERIOD = int(os.environ.get("TIMEOUT_PERIOD", 5))
