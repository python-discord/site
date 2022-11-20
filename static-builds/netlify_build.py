"""Build script to deploy project on netlify."""

# WARNING: This file must remain compatible with python 3.8

# This script performs all the actions required to build and deploy our project on netlify
# It depends on the following packages, which are set in the netlify UI:
# httpx == 0.23.0

import json
import os
import time
import zipfile
from pathlib import Path
from urllib import parse

import httpx


def raise_response(response: httpx.Response) -> None:
    """Raise an exception from a response if necessary."""
    if response.status_code // 100 != 2:
        try:
            print(response.json())
        except json.JSONDecodeError:
            pass

    response.raise_for_status()


if __name__ == "__main__":
    client = httpx.Client(
        follow_redirects=True,
        timeout=3 * 60,
    )

    owner, repo = parse.urlparse(os.getenv("REPOSITORY_URL")).path.lstrip("/").split("/")[0:2]

    download_url = "/".join([
        os.getenv("API_URL").rstrip("/"),
        "api/github/artifact",
        owner,
        repo,
        os.getenv("COMMIT_REF"),
        parse.quote(os.getenv("ACTION_NAME")),
        os.getenv("ARTIFACT_NAME"),
    ])
    print(f"Fetching download URL from {download_url}")
    response = client.get(download_url)
    raise_response(response)

    # The workflow is still pending, retry in a bit
    while response.status_code == 202:
        print(f"{response.json()['error']}. Retrying in 10 seconds.")
        time.sleep(10)
        response = client.get(download_url)

    raise_response(response)
    url = response.json()["url"]
    print(f"Downloading build from {url}")
    zipped_content = client.get(url)
    zipped_content.raise_for_status()

    zip_file = Path("temp.zip")
    zip_file.write_bytes(zipped_content.read())

    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        zip_ref.extractall("build")

    zip_file.unlink(missing_ok=True)

    print("Wrote artifact content to target directory.")
