"""Build script to deploy project on netlify."""

# WARNING: This file must remain compatible with python 3.8

# This script performs all the actions required to build and deploy our project on netlify
# It depends on the following packages, which are set in the netlify UI:
# httpx == 0.23.0

import json
import os
import zipfile
from pathlib import Path
from urllib import parse

import httpx

if __name__ == "__main__":
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
    response = httpx.get(download_url, follow_redirects=True)

    if response.status_code != 200:
        try:
            print(response.json())
        except json.JSONDecodeError:
            pass

        response.raise_for_status()

    url = response.json()["url"]
    print(f"Downloading build from {url}")
    zipped_content = httpx.get(url, follow_redirects=True)
    zipped_content.raise_for_status()

    zip_file = Path("temp.zip")
    zip_file.write_bytes(zipped_content.read())

    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        zip_ref.extractall("build")

    zip_file.unlink(missing_ok=True)

    print("Wrote artifact content to target directory.")
