"""Build script to deploy project on netlify."""

# WARNING: This file must remain compatible with python 3.8

# This script performs all the actions required to build and deploy our project on netlify
# It requires the following environment variable:

# TOKEN: A GitHub access token that can download the artifact.
#        For PAT, the only scope needed is `public_repos`

# It depends on the following packages, which are set in the netlify UI:
# httpx == 0.19.0

import os
import time
import zipfile
from pathlib import Path
from urllib import parse

import httpx

API_URL = "https://api.github.com"
OWNER, REPO = parse.urlparse(os.getenv("REPOSITORY_URL")).path.lstrip("/").split("/")[0:2]


def get_build_artifact() -> str:
    """Search for a build artifact, and return the download URL."""
    print("Fetching build URL.")

    if os.getenv("PULL_REQUEST").lower() == "true":
        print(f"Fetching data for PR #{os.getenv('REVIEW_ID')}")

        pull_url = f"{API_URL}/repos/{OWNER}/{REPO}/pulls/{os.getenv('REVIEW_ID')}"
        pull_request = httpx.get(pull_url)
        pull_request.raise_for_status()

        commit_sha = pull_request.json()["head"]["sha"]

        workflows_params = parse.urlencode({
            "event": "pull_request",
            "per_page": 100
        })

    else:
        commit_sha = os.getenv("COMMIT_REF")

        workflows_params = parse.urlencode({
            "event": "push",
            "per_page": 100
        })

    print(f"Fetching action data for commit {commit_sha}")

    workflows = httpx.get(f"{API_URL}/repos/{OWNER}/{REPO}/actions/runs?{workflows_params}")
    workflows.raise_for_status()

    for run in workflows.json()["workflow_runs"]:
        if run["name"] == "Build & Deploy Static Preview" and commit_sha == run["head_sha"]:
            print(f"Found action for this commit: {run['id']}\n{run['html_url']}")
            break
    else:
        raise Exception("Could not find the workflow run for this event.")

    polls = 0
    while polls <= 20:
        if run["status"] != "completed":
            print("Action isn't completed, sleeping for 30 seconds.")
            polls += 1
            time.sleep(30)

        elif run["conclusion"] != "success":
            print("Aborting build due to a failure in a previous CI step.")
            exit(0)

        else:
            print(f"Found artifact URL:\n{run['artifacts_url']}")
            return run["artifacts_url"]

        _run = httpx.get(run["url"])
        _run.raise_for_status()
        run = _run.json()

    raise Exception("Polled for the artifact workflow, but it was not ready in time.")


def download_artifact(url: str) -> None:
    """Download a build artifact from `url`, and unzip the content."""
    print("Fetching artifact data.")

    artifacts = httpx.get(url)
    artifacts.raise_for_status()
    artifacts = artifacts.json()

    if artifacts["total_count"] == "0":
        raise Exception(f"No artifacts were found for this build, aborting.\n{url}")

    for artifact in artifacts["artifacts"]:
        if artifact["name"] == "static-build":
            print("Found artifact with build.")
            break
    else:
        raise Exception("Could not find an artifact with the expected name.")

    zipped_content = httpx.get(artifact["archive_download_url"], headers={
        "Authorization": f"token {os.getenv('TOKEN')}"
    })
    zipped_content.raise_for_status()

    zip_file = Path("temp.zip")
    zip_file.write_bytes(zipped_content.read())

    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        zip_ref.extractall("build")

    zip_file.unlink(missing_ok=True)

    print("Wrote artifact content to target directory.")


if __name__ == "__main__":
    print("Build started")
    artifact_url = get_build_artifact()
    download_artifact(artifact_url)
