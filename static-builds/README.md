# Static Builds
This directory includes all the needed information to build and deploy static previews of the site.

Static deployments use [django-distill](https://github.com/meeb/django-distill) to build the static content.
The content is built in GitHub Actions, and is fetched and deployed by Netlify.


## Instructions
These are the configuration instructions to get started with static deployments.
They are split into two parts:

- [Building The Site](#building-the-site)
- [Deploying To Netlify](#deploying-to-netlify)


### Building The Site
To get started with building, you can use the following command:

```shell
poetry install
python -m pip install httpx==0.19.0
poetry run task static
```

Alternatively, you can use the [Dockerfile](/Dockerfile) and extract the build.

Both output their builds to a `build/` directory.

### Deploying To Netlify
To deploy to netlify, link your site GitHub repository to a netlify site, and use the settings below.
The netlify build script uses the site API to fetch and download the artifact, using a GitHub app that
can access the repo. The app must have the `actions` and `artifacts` scopes enabled.

### Netlify Settings
Build Command:
`python -m pip install httpx==0.23.0 && python static-builds/netlify_build.py`

Publish Directory:
`build`

**Environment Variables**

| Name           | Value                          | Description                                                                               |
|----------------|--------------------------------|-------------------------------------------------------------------------------------------|
| PYTHON_VERSION | 3.8                            | The python version. Supported options are defined by netlify [here][netlify build image]. |
| API_URL        | https://pythondiscord.com/     | The link to the API, which will be used to fetch the build artifacts.                     |
| ACTION_NAME    | Build & Publish Static Preview | The name of the workflow which will be used to find the artifact.                         |
| ARTIFACT_NAME  | static-build                   | The name of the artifact to download.                                                     |


[netlify build image]: https://github.com/netlify/build-image/tree/focal



Note that at this time, if you are deploying to netlify yourself, you won't have access to the
fa-icons pack we are using, which will lead to many missing icons on your preview.
You can either update the pack to one which will work on your domain, or you'll have to live with the missing icons.


> Warning: If you are modifying the [build script](./netlify_build.py), make sure it is compatible with Python 3.8.
